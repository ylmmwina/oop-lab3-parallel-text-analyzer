import queue
import threading
import time
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from core.parallel_processor import ParallelTextProcessor
from core.sequential_processor import SequentialTextProcessor


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TextAnalyzerApp(ctk.CTk):
    """
    @brief GUI-застосунок для паралельного аналізу текстових файлів.

    Інтерфейс запускає аналіз у background thread і отримує результати
    через queue.Queue. Це потрібно, щоб не оновлювати GUI напряму
    з робочого потоку.
    """

    def __init__(self):
        """
        @brief Ініціалізує головне вікно програми.
        """
        super().__init__()

        self.title("Parallel Text Analyzer — Lab 3")
        self.geometry("780x620")

        self.selected_folder: Path | None = None
        self.message_queue: queue.Queue = queue.Queue()
        self.worker_thread: threading.Thread | None = None

        self._build_ui()
        self.after(100, self._process_queue)

    def _build_ui(self) -> None:
        """
        @brief Створює елементи графічного інтерфейсу.
        """
        title = ctk.CTkLabel(
            self,
            text="Parallel Text Analyzer",
            font=("Arial", 24, "bold"),
        )
        title.pack(pady=16)

        self.folder_label = ctk.CTkLabel(
            self,
            text="No folder selected",
            font=("Arial", 14),
        )
        self.folder_label.pack(pady=6)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.select_button = ctk.CTkButton(
            button_frame,
            text="Select folder",
            command=self.select_folder,
            width=180,
        )
        self.select_button.grid(row=0, column=0, padx=8, pady=8)

        self.run_button = ctk.CTkButton(
            button_frame,
            text="Run comparison",
            command=self.run_comparison,
            width=180,
        )
        self.run_button.grid(row=0, column=1, padx=8, pady=8)

        self.progress_bar = ctk.CTkProgressBar(self, width=520)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Arial", 13),
        )
        self.status_label.pack(pady=4)

        self.output_box = ctk.CTkTextbox(self, width=700, height=390)
        self.output_box.pack(pady=14)

    def select_folder(self) -> None:
        """
        @brief Відкриває діалог вибору папки з текстовими файлами.
        """
        folder = filedialog.askdirectory()

        if not folder:
            return

        self.selected_folder = Path(folder)
        self.folder_label.configure(text=f"Selected: {self.selected_folder}")
        self._write_output("Folder selected.\n")

    def run_comparison(self) -> None:
        """
        @brief Запускає порівняння послідовної та паралельної обробки.
        """
        if self.worker_thread and self.worker_thread.is_alive():
            self._write_output("Analysis is already running.\n")
            return

        if self.selected_folder is None:
            self._write_output("Please select a folder first.\n")
            return

        files = sorted(self.selected_folder.glob("*.txt"))

        if not files:
            self._write_output("Selected folder does not contain .txt files.\n")
            return

        self.progress_bar.set(0)
        self.status_label.configure(text="Running...")
        self.run_button.configure(state="disabled")

        self.worker_thread = threading.Thread(
            target=self._worker_run_comparison,
            args=(files,),
            daemon=True,
        )
        self.worker_thread.start()

    def _worker_run_comparison(self, files: list[Path]) -> None:
        """
        @brief Виконує аналіз у фоновому потоці.
        @param files Список текстових файлів для аналізу.
        """
        try:
            self.message_queue.put(("status", "Running sequential processing..."))
            self.message_queue.put(("progress", 0.15))

            sequential_processor = SequentialTextProcessor()
            sequential_start = time.perf_counter()
            sequential_result = sequential_processor.process_files(files)
            sequential_time = time.perf_counter() - sequential_start

            self.message_queue.put(("status", "Running parallel processing..."))
            self.message_queue.put(("progress", 0.55))

            parallel_processor = ParallelTextProcessor(max_workers=4)
            parallel_start = time.perf_counter()
            parallel_result = parallel_processor.process_files(files)
            parallel_time = time.perf_counter() - parallel_start

            same_results = (
                sequential_result.file_count == parallel_result.file_count
                and sequential_result.line_count == parallel_result.line_count
                and sequential_result.word_count == parallel_result.word_count
                and sequential_result.char_count == parallel_result.char_count
                and sequential_result.word_frequencies == parallel_result.word_frequencies
            )

            speedup = sequential_time / parallel_time if parallel_time > 0 else 0

            report = self._format_report(
                sequential_result,
                sequential_time,
                parallel_time,
                speedup,
                same_results,
            )

            self.message_queue.put(("result", report))
            self.message_queue.put(("progress", 1.0))
            self.message_queue.put(("status", "Done"))

        except Exception as error:
            self.message_queue.put(("error", str(error)))

    def _process_queue(self) -> None:
        """
        @brief Обробляє повідомлення з робочого потоку в GUI-потоці.
        """
        try:
            while True:
                message_type, payload = self.message_queue.get_nowait()

                if message_type == "status":
                    self.status_label.configure(text=payload)

                elif message_type == "progress":
                    self.progress_bar.set(payload)

                elif message_type == "result":
                    self._write_output(payload)
                    self.run_button.configure(state="normal")

                elif message_type == "error":
                    self._write_output(f"Error: {payload}\n")
                    self.status_label.configure(text="Error")
                    self.run_button.configure(state="normal")

        except queue.Empty:
            pass

        self.after(100, self._process_queue)

    def _format_report(
        self,
        result,
        sequential_time: float,
        parallel_time: float,
        speedup: float,
        same_results: bool,
    ) -> str:
        """
        @brief Формує текстовий звіт для GUI.
        @param result Результат аналізу.
        @param sequential_time Час послідовної обробки.
        @param parallel_time Час паралельної обробки.
        @param speedup Прискорення паралельної версії.
        @param same_results Чи збігаються результати двох версій.
        @return Текстовий звіт.
        """
        top_words = "\n".join(
            f"  {word}: {count}"
            for word, count in result.top_words(10)
        )

        return (
            "Analysis completed.\n\n"
            f"Files: {result.file_count}\n"
            f"Lines: {result.line_count}\n"
            f"Words: {result.word_count}\n"
            f"Characters: {result.char_count}\n\n"
            f"Sequential time: {sequential_time:.6f} s\n"
            f"Parallel time: {parallel_time:.6f} s\n"
            f"Speedup: {speedup:.2f}x\n"
            f"Results equal: {same_results}\n\n"
            "Top words:\n"
            f"{top_words}\n"
        )

    def _write_output(self, text: str) -> None:
        """
        @brief Записує текст у поле результатів.
        @param text Текст для виведення.
        """
        self.output_box.delete("0.0", "end")
        self.output_box.insert("0.0", text)


if __name__ == "__main__":
    app = TextAnalyzerApp()
    app.mainloop()
