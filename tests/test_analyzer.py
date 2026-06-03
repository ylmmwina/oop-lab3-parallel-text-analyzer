from pathlib import Path

import pytest

from core.analyzer import TextAnalyzer
from core.exceptions import InvalidTextInputError


def test_analyze_valid_text_file(tmp_path):
    """
    @brief Перевіряє аналіз коректного текстового файлу.
    """
    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "Python is great.\nPython supports threads.",
        encoding="utf-8",
    )

    result = TextAnalyzer().analyze_file(file_path)

    assert result.file_count == 1
    assert result.line_count == 2
    assert result.word_count == 6
    assert result.char_count > 0
    assert result.word_frequencies["python"] == 2
    assert result.word_frequencies["threads"] == 1


def test_analyze_missing_file_raises_error():
    """
    @brief Перевіряє помилку для неіснуючого файлу.
    """
    missing_file = Path("missing_file.txt")

    with pytest.raises(InvalidTextInputError):
        TextAnalyzer().analyze_file(missing_file)


def test_analyze_non_txt_file_raises_error(tmp_path):
    """
    @brief Перевіряє помилку для файлу з неправильним розширенням.
    """
    file_path = tmp_path / "sample.md"
    file_path.write_text("# Markdown file", encoding="utf-8")

    with pytest.raises(InvalidTextInputError):
        TextAnalyzer().analyze_file(file_path)


def test_analyze_directory_raises_error(tmp_path):
    """
    @brief Перевіряє помилку, якщо передано директорію замість файлу.
    """
    with pytest.raises(InvalidTextInputError):
        TextAnalyzer().analyze_file(tmp_path)
