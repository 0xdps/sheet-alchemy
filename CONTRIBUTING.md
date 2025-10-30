# Contributing to G-ODM

Thank you for your interest in contributing to G-ODM! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.4 or higher
- Git
- Google Cloud Platform account (for testing with Google Sheets)

### Setting Up Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/0xdps/g-odm.git
   cd g-odm
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Set Up Google Sheets API Access**
   - Create a Google Cloud Platform project
   - Enable Google Sheets API
   - Create a service account and download the key file
   - Set the `GODM_AUTH_KEY_PATH` environment variable

## 📋 Development Guidelines

### Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep line length under 88 characters (Black formatter standard)

### Code Formatting

We recommend using these tools for consistent formatting:

```bash
# Install formatting tools
pip install black isort flake8

# Format code
black godm/
isort godm/

# Check style
flake8 godm/
```

### Project Structure

```
g-odm/
├── godm/                   # Main package
│   ├── __init__.py        # Package initialization
│   ├── model.py           # Base model classes
│   ├── field.py           # Field types
│   ├── _manager.py        # Query manager
│   ├── _meta.py           # Metaclass implementation
│   ├── _auth.py           # Authentication handling
│   ├── iterator.py        # Result iteration
│   ├── exceptions.py      # Custom exceptions
│   └── transformers.py    # Data transformation functions
├── test/                  # Test files and examples
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
├── README.md             # Documentation
├── CONTRIBUTING.md       # This file
└── PRIVACY.md            # Privacy policy
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest test/

# Run with coverage
python -m pytest --cov=godm test/

# Run specific test file
python -m pytest test/test_fields.py
```

### Writing Tests

- Write unit tests for all new features
- Include edge cases and error conditions
- Use descriptive test names
- Place tests in the `test/` directory
- Follow the naming convention: `test_*.py`

Example test structure:
```python
import unittest
from godm.field import StringField

class TestStringField(unittest.TestCase):
    def test_string_field_validation(self):
        field = StringField(name="Test")
        # Test implementation
        
    def test_string_field_empty_value(self):
        field = StringField(name="Test", allow_empty_or_null=True)
        # Test implementation
```

## 🐛 Reporting Issues

### Before Reporting

1. Check if the issue already exists in [GitHub Issues](https://github.com/0xdps/g-odm/issues)
2. Ensure you're using the latest version
3. Test with a minimal reproduction case

### Issue Template

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Minimal code example
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens  
- **Environment**: Python version, OS, library version
- **Error Messages**: Full error traceback if applicable

## 🔧 Making Changes

### Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. **Make Changes**
   - Write code following the style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Changes**
   ```bash
   python -m pytest test/
   flake8 godm/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new field type for URLs"
   # or
   git commit -m "fix: handle empty cells in BooleanField"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add CustomField for user-defined transformations
fix: handle None values in IntegerField validation
docs: update README with authentication examples
test: add integration tests for DateField parsing
```

## 📝 Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main

### PR Template

Include in your pull request:

1. **Description**: What changes are made and why
2. **Type of Change**: Bug fix, new feature, documentation, etc.
3. **Testing**: How the changes were tested
4. **Breaking Changes**: Any backwards-incompatible changes
5. **Checklist**: Confirm all requirements are met

### Review Process

1. Automated tests must pass
2. Code review by maintainers
3. Address feedback and make necessary changes
4. Final approval and merge

## 🎯 Areas for Contribution

### High Priority

- **Testing**: Improve test coverage
- **Documentation**: Examples and tutorials
- **Error Handling**: Better error messages
- **Performance**: Optimization opportunities

### New Features

- **Field Types**: JSONField, URLField, EmailField
- **Bulk Operations**: Create, update, delete multiple records
- **Query Features**: Aggregation, ordering, complex filters
- **Schema Management**: Migration tools

### Bug Fixes

- Check [open issues](https://github.com/0xdps/g-odm/issues) labeled `bug`
- Fix edge cases in existing functionality
- Improve error handling

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: Technical questions and bug reports
- **GitHub Discussions**: General questions and feature requests
- **Email**: For security issues, contact the maintainer directly

### Documentation

- Read the [README.md](README.md) thoroughly
- Check existing issues and discussions
- Look at example code in the `test/` directory

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain professionalism in all interactions

### Recognition

Contributors will be:
- Listed in release notes for significant contributions
- Mentioned in the README for major features
- Invited to become maintainers for sustained contributions

## 📄 Legal

By contributing to G-ODM, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing to G-ODM! Your efforts help make this library better for everyone. 🙏