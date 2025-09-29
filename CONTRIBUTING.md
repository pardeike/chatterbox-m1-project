# Contributing to Chatterbox M1 Project

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Code of Conduct

Be respectful and constructive in all interactions. This project aims to provide a helpful resource for deploying Chatterbox TTS on Apple Silicon.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

1. **Clear title** describing the issue
2. **Environment details**: macOS version, chip (M1/M2/M3), RAM
3. **Steps to reproduce** the problem
4. **Expected vs actual behavior**
5. **Error messages** or logs (if applicable)
6. **Screenshots** if relevant

Example:
```
Title: "Server fails to start with conda error on macOS 14"

Environment:
- MacBook Air M1, 8GB RAM
- macOS Sonoma 14.2
- Python 3.11 via Miniforge

Steps:
1. Run ./start_server.sh
2. Error appears: "conda: command not found"

Expected: Server starts successfully
Actual: Script exits with error code 1

Error log:
[paste error log here]
```

### Suggesting Enhancements

Open an issue with:

1. **Clear description** of the enhancement
2. **Use case**: Why would this be useful?
3. **Proposed solution** (if you have one)
4. **Alternatives considered**

### Pull Requests

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly** on M1 hardware if possible
5. **Update documentation** if needed
6. **Commit with clear messages**
7. **Push and create a Pull Request**

#### Pull Request Guidelines

- Keep changes focused and atomic
- Write clear commit messages
- Include tests if adding new functionality
- Update relevant documentation
- Ensure code works on Apple Silicon

#### Commit Message Format

```
type: Brief description

Longer explanation if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
fix: Resolve conda activation in start_server.sh

Added explicit conda initialization using the profile.d script
to ensure conda is available before activation.

Fixes #42
```

## Development Setup

### Prerequisites

- Apple Silicon Mac (M1, M2, or M3)
- macOS 11.0 or later
- Git
- Basic understanding of Python and bash

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/chatterbox-m1-project.git
cd chatterbox-m1-project

# Create a development branch
git checkout -b dev/your-feature

# Run setup
./setup_m1.sh

# Test your changes
conda activate chatterbox
python server.py
```

## Testing

Before submitting a PR:

1. **Test installation** from scratch if possible
2. **Test the web interface** at http://localhost:8000
3. **Test API endpoints** with curl or Python
4. **Test voice cloning** with reference audio
5. **Check for errors** in the server logs

### Running Tests

```bash
# Test basic TTS generation
python examples/basic_example.py

# Test voice cloning
python examples/voice_cloning_example.py

# Test API
python scripts/use_cloned_voice_api.py
```

## Documentation

When adding features:

1. Update README.md if needed
2. Add examples to relevant guides
3. Document new parameters or endpoints
4. Add comments to complex code
5. Update CHANGELOG.md

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

Example:
```python
def generate_speech_with_cache(text: str, params: dict) -> bytes:
    """
    Generate speech with caching to improve performance.
    
    Args:
        text: Text to synthesize
        params: Voice parameters (exaggeration, cfg_weight, temperature)
    
    Returns:
        Audio data as bytes
    
    Raises:
        ValueError: If text is empty or too long
    """
    if not text or len(text) > 1000:
        raise ValueError("Text must be 1-1000 characters")
    
    # Check cache first
    cache_key = generate_cache_key(text, params)
    if cached := get_from_cache(cache_key):
        return cached
    
    # Generate new audio
    audio = model.generate(text, **params)
    save_to_cache(cache_key, audio)
    
    return audio
```

## Apple Silicon Specific Considerations

When contributing code for M1 Macs:

1. **Test with MPS**: Ensure code works with Apple's Metal Performance Shaders
2. **CPU Fallback**: Some operations require CPU fallback
3. **Memory Efficiency**: Consider 8GB RAM constraints
4. **Conda ARM64**: Use ARM64-native packages when available
5. **PyTorch Compatibility**: Be aware of version requirements

## Areas for Contribution

### High Priority

- Docker support for easier deployment
- Additional language support and testing
- Performance optimizations
- Memory usage improvements
- Better error messages and logging

### Medium Priority

- Additional voice presets
- Batch processing API
- Real-time streaming support
- Better caching strategies
- Integration examples for popular frameworks

### Documentation

- Video tutorials
- More integration examples
- Troubleshooting guides
- Performance benchmarks
- Comparison with other TTS systems

## Questions?

- Open an issue for discussion
- Check existing issues for similar questions
- Review the documentation in the `docs/` folder

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Contributors will be acknowledged in the README.md file. Thank you for helping improve this project!