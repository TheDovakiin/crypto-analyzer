# Contributing to Crypto Analyzer

Thank you for your interest in contributing to the Crypto Analyzer project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When creating a bug report, include:

- **Clear and descriptive title**
- **Steps to reproduce the problem**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Screenshots or error messages** if applicable

### Suggesting Enhancements

We welcome feature requests! When suggesting enhancements:

- **Describe the feature clearly**
- **Explain why this feature would be useful**
- **Provide examples of how it would work**
- **Consider implementation complexity**

### Code Contributions

#### Setting Up Development Environment

1. **Fork the repository**
2. **Clone your fork:**

   ```bash
   git clone https://github.com/yourusername/crypto-analyzer.git
   cd crypto-analyzer
   ```

3. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

5. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

##### Code Style

- **Follow PEP 8** for Python code style
- **Use meaningful variable and function names**
- **Add docstrings** to all functions and classes
- **Keep functions focused** on a single responsibility
- **Limit line length** to 127 characters

##### Testing

- **Write tests** for new functionality
- **Ensure all tests pass** before submitting
- **Maintain good test coverage**
- **Test edge cases** and error conditions

##### Documentation

- **Update README.md** if adding new features
- **Add inline comments** for complex logic
- **Update docstrings** when changing function signatures
- **Include usage examples** for new features

#### Submitting Changes

1. **Test your changes:**

   ```bash
   pytest
   flake8 src/
   black --check src/
   ```

2. **Commit your changes:**

   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

3. **Push to your fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request:**
   - Use a clear title
   - Describe the changes in detail
   - Reference any related issues
   - Include screenshots for UI changes

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] **Code follows style guidelines**
- [ ] **All tests pass**
- [ ] **Documentation is updated**
- [ ] **No sensitive data is included**
- [ ] **Changes are focused and atomic**

### Pull Request Template

```markdown
## Description

Brief description of the changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes

## Screenshots (if applicable)
```

## 🏗️ Project Structure

```
crypto-analyzer/
├── src/                    # Source code
│   ├── scraper.py         # Data scraping
│   ├── analyzer.py        # Technical analysis
│   └── visualizer.py      # Visualization
├── tests/                 # Test files
├── docs/                  # Documentation
├── examples/              # Usage examples
└── scripts/               # Utility scripts
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/

# Run specific test file
pytest tests/test_analyzer.py

# Run with verbose output
pytest -v
```

### Writing Tests

- **Use descriptive test names**
- **Test both success and failure cases**
- **Mock external dependencies**
- **Use fixtures for common setup**

Example test structure:

```python
def test_calculate_sma():
    """Test Simple Moving Average calculation"""
    # Arrange
    data = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
    analyzer = CryptoAnalyzer()

    # Act
    result = analyzer.calculate_sma(data, period=3)

    # Assert
    assert len(result) == 5
    assert result.iloc[2] == 2.0  # SMA of [1,2,3]
```

## 📚 Documentation

### Code Documentation

- **Use Google-style docstrings**
- **Include type hints** for function parameters
- **Document exceptions** that may be raised
- **Provide usage examples**

Example:

```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index.

    Args:
        prices: Series of closing prices
        period: RSI period (default: 14)

    Returns:
        Series containing RSI values

    Raises:
        ValueError: If period is less than 2

    Example:
        >>> prices = pd.Series([1, 2, 3, 4, 5])
        >>> rsi = calculate_rsi(prices, period=3)
    """
```

### API Documentation

- **Document all public functions**
- **Include parameter descriptions**
- **Show return value types**
- **Provide usage examples**

## 🔒 Security

### Sensitive Data

- **Never commit API keys or secrets**
- **Use environment variables** for configuration
- **Check .gitignore** before committing
- **Use config.example.py** as a template

### Data Privacy

- **Respect rate limits** of external APIs
- **Handle user data securely**
- **Log sensitive operations** appropriately
- **Validate all inputs**

## 🚀 Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH**
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] **All tests pass**
- [ ] **Documentation is updated**
- [ ] **Version number is updated**
- [ ] **CHANGELOG.md is updated**
- [ ] **Release notes are prepared**

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

### Code of Conduct

- **Be respectful** and inclusive
- **Help others** learn and grow
- **Focus on the code**, not the person
- **Assume good intentions**

## 🎯 Areas for Contribution

### High Priority

- **Performance improvements**
- **Additional technical indicators**
- **Better error handling**
- **Enhanced documentation**

### Medium Priority

- **New data sources**
- **Advanced visualization features**
- **Machine learning integration**
- **Web dashboard**

### Low Priority

- **Code refactoring**
- **Style improvements**
- **Additional examples**
- **Translation support**

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes**
- **Project documentation**

Thank you for contributing to the Crypto Analyzer project! 🚀
