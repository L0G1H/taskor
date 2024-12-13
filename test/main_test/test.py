import pytest
import os
import json
import pyperclip
from unittest.mock import patch, mock_open
from taskor.taskor import (
    save_response,
    get_response_str,
    search_responses,
    RESPONSES_PATH,
    DEFAULT_MODEL_PATH,
    SYSTEM_PROMPT_PATH,
)

# Test data
TEST_RESPONSES = [
    {"nr": 1, "prompt": "test prompt 1", "response": "test response 1"},
    {"nr": 2, "prompt": "test prompt 2", "response": "test response 2"},
]


@pytest.fixture
def mock_responses_file():
    with patch("builtins.open", mock_open(read_data=json.dumps(TEST_RESPONSES))) as mock_file:
        yield mock_file


def test_save_response(mock_responses_file):
    prompt = "test prompt"
    response = "test response"

    with patch("json.load", return_value=TEST_RESPONSES):
        save_response(prompt, response)

        # Check if the file was opened for writing
    mock_responses_file.assert_called_with(RESPONSES_PATH, "w", encoding="utf-8")


def test_get_response_str_valid_number(mock_responses_file):
    with patch("json.load", return_value=TEST_RESPONSES):
        response = get_response_str("1")
        assert response == "test response 1"


def test_get_response_str_invalid_number(mock_responses_file):
    with patch("json.load", return_value=TEST_RESPONSES):
        response = get_response_str("999")
        assert response == ""


def test_get_response_str_latest(mock_responses_file):
    with patch("json.load", return_value=TEST_RESPONSES):
        response = get_response_str("")
        assert response == "test response 2"


def test_search_responses(mock_responses_file, capsys):
    with patch("json.load", return_value=TEST_RESPONSES):
        search_responses("test prompt 1")
        captured = capsys.readouterr()
        assert "Found" in captured.out
        assert "test prompt 1" in captured.out


def test_search_responses_no_matches(mock_responses_file, capsys):
    with patch("json.load", return_value=TEST_RESPONSES):
        search_responses("nonexistent")
        captured = capsys.readouterr()
        assert "No matches found" in captured.out


@pytest.mark.parametrize(
    "file_path,content",
    [
        (RESPONSES_PATH, "[]"),
        (DEFAULT_MODEL_PATH, "gpt-3.5-turbo"),
        (SYSTEM_PROMPT_PATH, "You are a helpful assistant."),
    ],
)
def test_file_existence(file_path, content):
    assert os.path.exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        assert isinstance(file_content, str)


def test_clipboard_integration():
    test_text = "Test clipboard text"
    pyperclip.copy(test_text)
    assert pyperclip.paste() == test_text


@pytest.mark.parametrize(
    "prompt,expected_error",
    [
        ("", "Invalid syntax"),
        ("nonexistent", "Given response nr is out of bounds"),
    ],
)
def test_error_handling(prompt, expected_error, capsys):
    with patch("json.load", return_value=TEST_RESPONSES):
        get_response_str(prompt)
        captured = capsys.readouterr()
        assert expected_error in captured.out


if __name__ == "__main__":
    pytest.main(["-v"])