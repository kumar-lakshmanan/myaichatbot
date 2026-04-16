# MyAIChatBot - AI-Powered Development Assistant

An intelligent AI chatbot framework built with Python that integrates with Ollama for advanced conversational capabilities and automated tool execution to assist with development activities.

[![PyPI](https://img.shields.io/pypi/v/myaichatbot.svg)](https://pypi.org/project/myaichatbot)
[![License](https://img.shields.io/github/license/kayma/myaichatbot.svg)](LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/kayma/myaichatbot/test.yml?label=tests)](https://github.com/kayma/myaichatbot/actions)

## Quick Start

```bash
# Download/Install ollama
https://ollama.com/download

# Download/Pull ai models for ollama
https://docs.ollama.com/cli

ollama pull qwen3-coder:480b-cloud

# Install the package
pip install myaichatbot

# Set environment variables
export OLLAMA_API_KEY="your-api-key-here"

# Run the application
myaichatbot
```

```python
# Basic usage example
from myaichatbot.main import MyAIChatBot

mcb = MyAIChatBot()
mcb.initialize()
mcb.chat("Can you help me understand this code?")
print(mcb.get_response())
```

## Project Overview

MyAIChatBot is an extensible AI assistant platform designed specifically for software development workflows. It combines the power of large language models with practical tool execution capabilities to provide intelligent assistance for coding tasks, project analysis, and technical problem-solving.

The framework provides:
- Intelligent conversations with context awareness
- Automated tool execution for file operations and web searches
- Conversation history management
- Reference file integration for contextual responses
- Extensible architecture for custom tools

### Key Features

- **Intelligent Conversations**: Natural language understanding powered by Ollama models
- **Tool Execution**: Automated execution of file operations, web searches, and system commands
- **Context Awareness**: Maintains conversation history and project context
- **Extensible Architecture**: Modular design for easy customization and enhancement
- **Development Focused**: Specifically designed for assisting with programming tasks
- **Reference Integration**: Ability to include project files as reference context

## Installation

### Prerequisites

- Python 3.8+
- Ollama (with required models installed)
- Required Python packages

### Installation Options

#### Option 1: Install from PyPI
```bash
pip install myaichatbot
```

#### Option 2: Install from source
```bash
git clone https://github.com/kayma/myaichatbot.git
cd myaichatbot
pip install .
```

#### Option 3: Install in development mode
```bash
git clone https://github.com/kayma/myaichatbot.git
cd myaichatbot
pip install -e .
```

### Setup Steps

1. Install required Ollama models:
```bash
ollama pull qwen3-coder:480b-cloud
ollama pull gpt-oss:20b-cloud
```

2. Set up environment variables:
```bash
export OLLAMA_API_KEY="your-api-key-here"
```

## Usage Examples

### Command Line Usage

```bash
# Run the application
python -m myaichatbot.main
```

### Programmatic Usage

```python
from myaichatbot.main import MyAIChatBot

mcb = MyAIChatBot()
mcb.initialize()
mcb.chat("Explain how this project works")
print(mcb.get_response())
```

### Project Analysis

```python
from myaichatbot.main import MyAIChatBot

mcb = MyAIChatBot()
mcb.include_reference_files = 1
mcb.reference_files_paths = ["/path/to/your/project"]
mcb.reference_files_exclude = ['.pyc', '.log', '.__pycache__']
mcb.initialize()
mcb.chat("Can you analyze this project and explain its structure?")
print(mcb.get_response())
```

### Code Assistance with Tools

```python
from myaichatbot.main import MyAIChatBot

mcb = MyAIChatBot()
mcb.initialize()
# The AI can automatically use tools like file operations and web search
mcb.chat("Create a new Python file that implements a simple calculator")
print(mcb.get_response())
```

## API Reference

### Main Classes

| Class | Description |
|-------|-------------|
| `MyAIChatBot()` | Main chatbot interface with initialization and conversation methods |
| `Messages()` | Message handling system for managing conversation context |
| `Tools()` | Tool management system for registering and executing tools |
| `Utilities()` | Utility functions for file operations and helper methods |
| `Conversation()` | Conversation history management |
| `kTools.KTools()` | Core utility framework (singleton pattern) |

### Core Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `chat()` | `chat(qry: str)` | Process a user query through the AI system |
| `get_response()` | `get_response()` | Retrieve the final response from the AI |
| `initialize()` | `initialize()` | Initialize the AI agent and components |
| `addTool()` | `addTool(fn)` | Register a new tool function |
| `getFileContent()` | `getFileContent(fileName)` | Read content from a file |
| `writeFileContent()` | `writeFileContent(fileName, data)` | Write content to a file |

### Configuration Options

Environment variables:
- `OLLAMA_API_KEY`: Required API key for Ollama services
- `K_ISPROD`: Set to 1 for production mode, 0 for development

Configuration files:
- `config.json`: Main application configuration
- `lookup.py`: Application constants and settings

Advanced configuration options:
```python
# Enable conversation saving
mcb.save_conversation = 1
mcb.conversation_file_path = "./conversations"

# Include reference files in context
mcb.include_reference_files = 1
mcb.reference_files_paths = ["/path/to/project"]
mcb.reference_files_exclude = ['.pyc', '.log']

# Adjust AI behavior
mcb.repeatCoreCallingCountLimit = 5
mcb.ai_definition = "Custom AI personality definition"

# Control verbosity
mcb.verbose = 1
```

## Project Structure

```
myaichatbot/
├── myaichatbot/              # Main package
│   ├── __init__.py
│   ├── main.py               # Main application entry point
│   ├── lookup.py             # Application constants and settings
│   ├── config.json           # Application configuration
│   ├── prompt.txt            # Default prompt template
│   ├── core/                 # Core components
│   │   ├── __init__.py
│   │   ├── message.py        # Message handling system
│   │   └── conversation.py   # Conversation history management
│   ├── tools/                # Tool management system
│   │   ├── __init__.py
│   │   ├── tools.py          # Main tools interface
│   │   └── custom_tools/     # Custom tool implementations
│   │       ├── __init__.py
│   │       └── web_action.py # Web search and fetch tools
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   └── utils.py          # Helper functions
│   └── models/               # AI model interfaces
│       ├── __init__.py
├── setup.py                  # Setup script for packaging
├── pyproject.toml            # Modern Python packaging configuration
├── requirements.txt          # Python package dependencies
├── MANIFEST.in              # Package manifest
└── README.md                # This file
```

### Component Details

1. **myaichatbot/main.py**: Main application entry point with MyAIChatBot class and CLI interface.

2. **myaichatbot/core/message.py**: Manages conversation messages with filtering for duplicates and proper message structuring.

3. **myaichatbot/core/conversation.py**: Handles saving and retrieving conversation history for context awareness.

4. **myaichatbot/tools/tools.py**: Tool registration and execution system that allows the AI to use functions like file operations and web searches.

5. **myaichatbot/tools/custom_tools/web_action.py**: Implementation of web search and fetch tools using Ollama.

6. **myaichatbot/utils/utils.py**: Utility functions including recursive file reading and AI completion checking.

7. **myaichatbot/lookup.py**: Application constants and settings.

8. **commonlib/kTools.py**: Core utility framework implementing singleton pattern with extensive helper functions for logging, file operations, configuration management, etc. (external dependency)

## Requirements

```text
ollama>=0.1.0
```

## Contributing

1. Clone the repo:
```bash
git clone https://github.com/kayma/myaichatbot.git
cd myaichatbot
```

2. Install in development mode:
```bash
pip install -e .
```

3. Make your changes

4. Submit a pull request with a detailed description of your changes

## License

MIT – see `LICENSE`

## Author

Kumaresan Lakshmanan (kayma) – <kaymatrix@gmail.com>  
⏰ v0.1.0 · 2026-03-26