import unittest
from unittest.mock import patch, mock_open, MagicMock
from utils.assistant_api import get_completion


class TestAssistantAPI(unittest.TestCase):
    @patch("utils.assistant_api.Anthropic")
    def test_claude_completion(self, mock_anthropic):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Test response")]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        result = get_completion("claude-3", "Test prompt")
        self.assertEqual(result, "Test response")

    @patch("utils.assistant_api.OpenAI")
    def test_openai_completion(self, mock_openai):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        result = get_completion("gpt-4", "Test prompt")
        self.assertEqual(result, "Test response")

    @patch("builtins.open", mock_open(read_data="System prompt text"))
    def test_system_prompt_inclusion(self):
        with patch("utils.assistant_api.Anthropic") as mock_anthropic:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text="Test response")]
            mock_anthropic.return_value.messages.create.return_value = mock_response

            result = get_completion("claude-3", "Test prompt", is_system_prompt=True)
            self.assertEqual(result, "Test response")


if __name__ == "__main__":
    unittest.main()        