# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-28

### Added
- Initial release of Chatterbox TTS deployment for M1 MacBook Air
- Automated setup script (`setup_m1.sh`) for one-command installation
- FastAPI web server with responsive UI
- REST API for text-to-speech generation
- Voice cloning support with reference audio
- Voice library system for managing multiple synthetic voices
- Multilingual support (20+ languages)
- Apple Silicon MPS acceleration with CPU fallback
- Comprehensive documentation and guides
- Example scripts for common use cases
- Command-line tools for voice generation
- Health check and monitoring endpoints

### Fixed
- PyTorch/TorchVision compatibility issues on Apple Silicon
- `operator torchvision::nms does not exist` error
- `rope_scaling` configuration format issues
- Transformers version compatibility
- NumPy version conflicts
- SymPy dependency resolution
- Conda environment activation in scripts
- MPS fallback for unsupported operations

### Optimized
- Memory usage for MacBook Air constraints
- Model loading and caching
- Text chunking for long-form content
- Server startup time
- API response times

---

## Release Notes

### Version 1.0.0 - Initial Release

Production-ready release of Chatterbox TTS deployment optimized for Apple Silicon M1 MacBook Air. Includes comprehensive setup automation, web interface, REST API, and integration tools.

**Key Features:**
- Stable text-to-speech generation with MPS acceleration
- Voice cloning with 10-30 second reference clips
- Multiple integration patterns for various use cases
- Complete documentation and troubleshooting guides

**Known Limitations:**
- Some PyTorch operations require CPU fallback (automatically handled)
- Maximum text length of 1000 characters per request (configurable)
- First model load takes 30-60 seconds (subsequent loads are instant)
- Requires PYTORCH_ENABLE_MPS_FALLBACK=1 for full functionality

**Performance:**
- Model loading: 30-60 seconds (first time only)
- Generation speed: 2-5 seconds for short sentences
- Memory usage: 3-4GB
- Supports voice cloning with 10-30 second reference clips