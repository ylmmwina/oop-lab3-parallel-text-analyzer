from pathlib import Path

from core.benchmark import BenchmarkRunner


def main() -> None:
    """
    @brief Запускає benchmark для sample_texts і зберігає CSV-результати.
    """
    dataset_path = Path("data/sample_texts")
    output_path = Path("results/benchmark-results.csv")

    runner = BenchmarkRunner(worker_counts=[1, 2, 4])
    rows = runner.run_for_dataset(dataset_path)
    runner.save_csv(rows, output_path)

    print(f"Benchmark results saved to {output_path}")

    for row in rows:
        print(
            f"{row.dataset_name}: "
            f"files={row.file_count}, "
            f"workers={row.worker_count}, "
            f"sequential={row.sequential_time:.6f}s, "
            f"parallel={row.parallel_time:.6f}s, "
            f"speedup={row.speedup:.2f}x, "
            f"equal={row.results_equal}"
        )


if __name__ == "__main__":
    main()
