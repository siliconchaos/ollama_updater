# Ollama Model Updater

A utility to update all installed Ollama models with progress tracking and rich terminal output.

## Installation

Install using pipx:

```bash
# Install from PyPI (when or if published)
# pipx install ollama-updater

# Install from Git
pipx install git+https://github.com/siliconchaos/ollama_updater.git

# Install from Git with specific branch/tag
pipx install git+https://github.com/siliconchaos/ollama_updater.git@main
pipx install git+https://github.com/siliconchaos/ollama_updater.git@v0.1.0

# Install in development mode
pipx install --editable git+https://github.com/siliconchaos/ollama_updater.git

# Run without installing
pipx run --spec git+https://github.com/siliconchaos/ollama_updater.git ollama-updater
```

## Usage

```bash
ollama-updater [--log-level LEVEL]
```

Options:

- `--log-level, -l`: Set logging level (DEBUG, INFO, WARNING, ERROR)
