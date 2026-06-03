from pathlib import Path


TEXT_TEMPLATE = '''
Python supports object-oriented programming.
Multithreading can improve processing of many files.
Sequential and parallel algorithms must return the same result.
Text analysis counts lines, words, characters, and word frequencies.
Benchmark results help compare different execution modes.
'''


def create_dataset(base_path: Path, dataset_name: str, file_count: int, repetitions: int) -> None:
    '''
    @brief Створює dataset з текстовими файлами для benchmark.
    @param base_path Базова директорія для datasets.
    @param dataset_name Назва dataset.
    @param file_count Кількість файлів.
    @param repetitions Кількість повторень текстового шаблону у файлі.
    '''
    dataset_path = base_path / dataset_name
    dataset_path.mkdir(parents=True, exist_ok=True)

    for index in range(1, file_count + 1):
        file_path = dataset_path / f'text_{index:03}.txt'
        content = (TEXT_TEMPLATE * repetitions).strip()
        file_path.write_text(content, encoding='utf-8')


def main() -> None:
    '''
    @brief Генерує datasets різного розміру для benchmark-вимірювань.
    '''
    base_path = Path('data/generated')

    create_dataset(base_path, 'small', file_count=5, repetitions=10)
    create_dataset(base_path, 'medium', file_count=25, repetitions=40)
    create_dataset(base_path, 'large', file_count=60, repetitions=80)

    print('Generated benchmark datasets:')
    print('- data/generated/small')
    print('- data/generated/medium')
    print('- data/generated/large')


if __name__ == '__main__':
    main()
