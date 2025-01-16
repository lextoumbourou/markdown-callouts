# markdown-obsidian-callouts

[![Tests](https://github.com/lextoumbourou/markdown-obsidian-callouts/actions/workflows/test.yml/badge.svg)](https://github.com/lextoumbourou/markdown-obsidian-callouts/actions/workflows/test.yml)

**[Python-Markdown](https://python-markdown.github.io/) Extension: use Obsidian Style callouts in Markdown**

![Example of Obsidian Callout from the Obsidian docs page](image.png)


This plugin inputs the Obsidian syntax and output format for [Callouts](https://help.obsidian.md/Editing+and+formatting/Callouts)

Originally a fork of [markdown-callouts](https://github.com/oprypin/markdown-callouts) but now a completely separate package. The major difference is that the output format no longer matches Admonitions.

## Installation

```shell
pip install markdown-obsidian-callouts
```

## Development Setup

### Running tests

```shell
git clone https://github.com/lextoumbourou/markdown-obsidian-callouts
cd markdown-obsidian-callouts

uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

pytest
```

### Publishing

To publish updates to PyPI:

1. Ensure you have a PyPI account and the required tools:
2. Update the version in `pyproject.toml`
3. Build the package:

    ```bash
    python -m build
    ```

4. Upload to PyPI:

    ```bash
    python -m twine upload dist/*
    ```

    (API token is required)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
