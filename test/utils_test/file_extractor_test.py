import unittest
from unittest.mock import patch, mock_open, MagicMock
import taskor.utils.file_extractor as ext


class TestFileExtractor(unittest.TestCase):
    def test_extract_text_from_txt(self):
        test_content = "Test content"
        with patch("builtins.open", mock_open(read_data=test_content)):
            result = ext.extract_text_from_txt("test.txt")
            self.assertEqual(result, test_content)


    @patch("builtins.open", return_value=MagicMock())
    @patch("utils.file_extractor.PyPDF2.PdfReader")
    def test_extract_text_from_pdf(self, mock_pdf_reader, mock_open):
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Test PDF content"
        mock_pdf_reader.return_value.pages = [mock_page]

        result = ext.extract_text_from_pdf("test.pdf")

        self.assertIn("Test PDF content", result)

        mock_open.assert_called_once_with("test.pdf", "rb")

    @patch("utils.file_extractor.Document")
    def test_extract_text_from_doc(self, mock_document):
        mock_doc = MagicMock()
        mock_doc.paragraphs = [MagicMock(text="Test paragraph")]
        mock_document.return_value = mock_doc

        result = ext.extract_text_from_doc("test.docx")
        self.assertEqual(result, "Test paragraph")

    @patch("utils.file_extractor.Image")
    @patch("utils.file_extractor.pytesseract")
    def test_extract_text_from_image(self, mock_pytesseract, mock_image):
        type(mock_image)
        mock_pytesseract.image_to_string.return_value = "Test OCR text"

        result = ext.extract_text_from_image("test.png")
        self.assertEqual(result, "Test OCR text")

    def test_extract_text_from_json(self):
        test_json = {"key": "value"}
        type(test_json)
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            result = ext.extract_text_from_json("test.json")
            self.assertIn("key", result)
            self.assertIn("value", result)

    @patch("utils.file_extractor.extract_text_from_binary")
    def test_fallback_to_binary(self, mock_binary):
        mock_binary.return_value = "Binary content"
        result = ext.extract_text_from_file("unknown.xyz")
        self.assertIn("Binary content", result)


if __name__ == "__main__":
    unittest.main()
