# taskor CLI

A command-line interface tool for task automation and prompt management.

## Features

- Execute prompts with GPT models
- Save and manage response history
- Search through previous responses
- Include external files in prompts
- Copy responses to clipboard
- Customize system prompts and default models

## Installation

```bash
git clone https://github.com/L0G1H/taskor.git
cd taskor
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
taskor "your prompt here"
```

### Options

- `-m, --model`: Specify the GPT model (default: configured in default_model.txt)
- `-f, --add-files`: Include external files in the prompt
- `-i, --incognito`: Don't save the response in history
- `-p, --paste`: Include clipboard content in the prompt
- `-n, --no-prompt`: Skip system prompt
- `-s, --search`: Search through saved responses
- `-c, --copy`: Copy a response to clipboard (default: last response)
- `--change-system-prompt`: Update the system prompt
- `--change-default-model`: Change the default model
- `--delete-history`: Clear response history

### Examples

```bash
# Basic prompt
python taskor.py "Write a hello world program in Python"

# Use specific model
python taskor.py -m gpt-4 "Explain quantum computing"

# Include files in prompt
python taskor.py -f "Review this code"

# Search through responses
python taskor.py -s "python"

# Copy last response to clipboard
python taskor.py -c

# Change system prompt
python taskor.py --change-system-prompt "New system prompt"
```