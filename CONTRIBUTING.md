# Contributing to Telegram Ad Bot 🤝

Thank you for your interest in contributing to Telegram Ad Bot! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/telegram-ad-bot.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes
5. **Test** your changes: `python test_bot.py`
6. **Commit** your changes: `git commit -m 'Add amazing feature'`
7. **Push** to your branch: `git push origin feature/amazing-feature`
8. **Open** a Pull Request

## 📋 Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- A Telegram account (for testing)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/telegram-ad-bot.git
cd telegram-ad-bot

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_bot.py
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python test_bot.py

# Run specific test modules
python -c "import test_bot; test_bot.test_dependencies()"
```

### Test Coverage
We aim for high test coverage. Please add tests for new features:
- Unit tests for individual functions
- Integration tests for bot interactions
- Mock tests for external dependencies

## 📝 Code Style

### Python Style Guide
We follow PEP 8 with some modifications:
- Maximum line length: 127 characters
- Use type hints where possible
- Document all public functions and classes

### Code Formatting
```bash
# Install formatting tools
pip install black flake8

# Format code
black .

# Check code style
flake8 .
```

## 🏗️ Project Structure

```
telegram-ad-bot/
├── launcher.py              # Main entry point
├── main.py                  # Single account bot
├── multi_bot.py             # Multi-account manager
├── host.py                  # Hosting script
├── test_bot.py              # Test suite
├── setup.py                 # Setup script
├── requirements.txt         # Dependencies
├── README.md               # Main documentation
├── README_MULTI.md         # Multi-account guide
├── CONTRIBUTING.md         # This file
├── LICENSE                 # MIT License
└── assets/
    ├── config.toml         # Single bot config
    ├── accounts.json       # Multi-account config
    ├── groups.txt          # Groups list
    └── sessions/           # Saved sessions
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Bug fixes
- [ ] Performance improvements
- [ ] Security enhancements
- [ ] Documentation updates

### Medium Priority
- [ ] New features
- [ ] UI/UX improvements
- [ ] Additional hosting options
- [ ] More configuration options

### Low Priority
- [ ] Code refactoring
- [ ] Additional test coverage
- [ ] Performance optimizations

## 🐛 Bug Reports

### Before Submitting
1. Check if the bug has already been reported
2. Try to reproduce the bug with the latest version
3. Check the troubleshooting section in README.md

### Bug Report Template
```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 10, macOS, Ubuntu]
- Python Version: [e.g. 3.9.0]
- Bot Version: [e.g. 2.0.0]

**Additional Context**
Add any other context about the problem here.
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
How would this feature be used? What problem does it solve?

**Proposed Implementation**
Any ideas on how this could be implemented?

**Additional Context**
Add any other context or screenshots about the feature request.
```

## 🔄 Pull Request Process

### Before Submitting
1. **Test** your changes thoroughly
2. **Update** documentation if needed
3. **Add** tests for new features
4. **Check** code style with flake8 and black
5. **Update** version numbers if needed

### PR Template
```markdown
**Description**
Brief description of changes made.

**Type of Change**
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

**Testing**
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

**Screenshots**
If applicable, add screenshots to help explain your changes.

**Additional Notes**
Add any other context about the pull request here.
```

## 📚 Documentation

### Writing Documentation
- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep documentation up to date

### Documentation Structure
- `README.md` - Main project documentation
- `README_MULTI.md` - Multi-account specific guide
- `CONTRIBUTING.md` - This file
- Inline code comments
- Docstrings for functions and classes

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## 📞 Getting Help

### Communication Channels
- **Issues**: [GitHub Issues](https://github.com/yourusername/telegram-ad-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/telegram-ad-bot/discussions)
- **Wiki**: [Documentation Wiki](https://github.com/yourusername/telegram-ad-bot/wiki)

### Before Asking for Help
1. Check the documentation
2. Search existing issues
3. Try to reproduce the problem
4. Provide detailed information

## 🎉 Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

## 📄 License

By contributing to Telegram Ad Bot, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Telegram Ad Bot! 🚀 