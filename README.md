# Taskor: Intelligent Task Automation CLI

## Overview

Taskor is a powerful, flexible command-line interface (CLI) tool designed for task automation, prompt management, and intelligent text processing. It leverages various AI models and offers robust file handling capabilities.

## Features

- 🤖 AI-Powered Text Generation
- 📄 Multi-File Text Extraction
- 📋 Clipboard Integration
- 💾 Response History Management
- 🔍 Response Search Functionality
- 🔑 Customizable System Prompts and Models

## Prerequisites

- Python 3.12+
- Poetry (dependency management)

## Installation

### Clone the Repository
```bash
git clone https://github.com/L0G1H/taskor.git
cd taskor
poetry install
```

## Usage

### Basic Prompt
```bash
poetry run taskor "Write a Python function to reverse a string"
```

### Advanced Options
- `-m, --model`: Specify AI model
- `-f, --add-files`: Include external files
- `-i, --incognito`: Prevent saving response
- `-p, --paste`: Use clipboard content
- `-s, --search`: Search response history
- `-c, --copy`: Copy specific response

### Examples
```bash
# Generate code with GPT-4
poetry run taskor -m gpt-4 "Create a Flask API endpoint"

# Include file contents in context
poetry run taskor -f "Summarize this document"

# Search response history
poetry run taskor -s "python"
```

## Configuration

### System Prompt
```bash
poetry run taskor --change-system-prompt "You are a helpful coding assistant"
```

### Default Model
```bash
poetry run taskor --change-default-model "anthropic/claude-2"
```

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.