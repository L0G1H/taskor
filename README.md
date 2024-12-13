# Taskor

Taskor is a powerful, flexible command-line interface (CLI) tool designed for task automation, prompt management, and intelligent text processing. It leverages various AI models and offers robust file handling capabilities.

## Features

- 🤖 AI-Powered Text Generation
- 📄 Multi-File Text Extraction
- 📋 Clipboard Integration
- 💾 Response History Management
- 🔍 Response Search Functionality
- 🔑 Customizable System Prompts and Models

## Installation
```bash
git clone https://github.com/L0G1H/taskor.git
cd taskor
poetry install
```

## Help
```bash
usage: taskor [-h] [-m MODEL] [-f] [-i] [-p] [-n] [-s] [-c] [--change-system-prompt] [--change-default-model] [--delete-history] [prompt ...]

Taskor CLI Tool

positional arguments:
  prompt                input

options:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        model to use (default - claude-3-5-haiku-latest)
  -f, --add-files       add external files
  -i, --incognito       not to save response
  -p, --paste           include current paste in the prompt
  -n, --no-prompt       pass request without a system prompt
  -s, --search          search for a specific term in saved responses
  -c, --copy            copy a specific response (default - last)
  --change-system-prompt
                        change system prompt
  --change-default-model
                        change default model
  --delete-history      delete request history
```

## Usage

### Basic Prompt
```bash
taskor Write a Python function to reverse a string
```
### Generate code with GPT-4
```bash
taskor -m gpt-4 Create a Flask API endpoint
```

### Include file contents in context
```bash
taskor -f Summarize this document
```

### Search response history
```bash
taskor -s python
```

### Change system Prompt
```bash
taskor --change-system-prompt You are a helpful coding assistant
```

### Change default Model
```bash
taskor --change-default-model claude-3-5-sonnet-latest
```

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
