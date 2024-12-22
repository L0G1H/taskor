import unittest
from unittest.mock import patch
from taskor.utils.file_selector import get_file_paths


class TestFileSelector(unittest.TestCase):
    @patch("utils.file_selector.QApplication")
    @patch("utils.file_selector.QFileDialog")
    def test_get_file_paths(self, mock_dialog, mock_app):
        expected_files = ["/path/to/file1.txt", "/path/to/file2.pdf"]
        mock_dialog.getOpenFileNames.return_value = (expected_files, None)

        result = get_file_paths()

        self.assertEqual(result, expected_files)
        mock_dialog.getOpenFileNames.assert_called_once()
        mock_app.return_value.exit.assert_called_once()


if __name__ == "__main__":
    unittest.main()