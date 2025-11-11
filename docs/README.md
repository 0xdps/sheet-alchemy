# SheetAlchemy Documentation

This directory contains the Sphinx documentation for SheetAlchemy.

## Building Documentation Locally

### Prerequisites

Install documentation dependencies:

```bash
pip install -r requirements.txt
```

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be in `_build/html/`. Open `_build/html/index.html` in your browser.

### Build Other Formats

```bash
# PDF (requires LaTeX)
make latexpdf

# ePub
make epub

# Plain text
make text
```

### Clean Build Files

```bash
make clean
```

## Read the Docs

The documentation is automatically built and hosted on [Read the Docs](https://readthedocs.org/) when changes are pushed to the repository.

Configuration file: `.readthedocs.yaml` (in project root)

## Documentation Structure

```
docs/
├── conf.py                 # Sphinx configuration
├── index.rst               # Main documentation page
├── installation.rst        # Installation guide
├── quickstart.rst          # Quick start tutorial
├── authentication.rst      # Authentication setup
├── models.rst              # Models guide
├── fields.rst              # Fields reference
├── querying.rst            # Querying guide
├── advanced.rst            # Advanced features
├── api/                    # API reference (auto-generated)
├── tutorials/              # Detailed tutorials
└── requirements.txt        # Documentation dependencies
```

## Contributing to Documentation

1. Edit `.rst` files in the `docs/` directory
2. Build locally to verify changes: `make html`
3. Submit a pull request

### Writing Style

- Use clear, concise language
- Include code examples
- Add cross-references to related topics
- Use consistent formatting
