# Publishing to GitHub

This guide walks you through publishing your Chatterbox M1 project to GitHub.

## Prerequisites

- GitHub account
- Git installed on your Mac
- Project fully set up and tested

## Quick Start

```bash
# Navigate to project directory
cd ~/chatterbox-m1-project

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Chatterbox TTS for M1 MacBook Air"

# Create GitHub repository (via web or CLI)
# Then add remote and push:
git remote add origin https://github.com/mkoker/chatterbox-m1-project.git
git branch -M main
git push -u origin main
```

## Detailed Steps

### Step 1: Prepare Your Repository

Before publishing, ensure your project is clean:

```bash
# Check what files will be included
git status

# Review .gitignore to ensure sensitive files are excluded
cat .gitignore

# Remove any test output files
rm -f outputs/*.wav
rm -f test*.wav
```

### Step 2: Initialize Git

```bash
cd ~/chatterbox-m1-project
git init
```

### Step 3: Configure Git (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Add Files

```bash
# Add all files (respecting .gitignore)
git add .

# Review what's being added
git status

# If you need to exclude something:
echo "file_to_exclude.txt" >> .gitignore
git add .gitignore
```

### Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: Chatterbox TTS deployment for M1 MacBook Air

- Complete installation scripts for Apple Silicon
- FastAPI web server with UI
- REST API for TTS and voice cloning
- Voice library system
- Comprehensive documentation
- Example scripts and integration guides"
```

### Step 6: Create GitHub Repository

**Option A: Via GitHub Website**

1. Go to https://github.com/new
2. Repository name: `chatterbox-m1-project` (or your preferred name)
3. Description: "Production-ready Chatterbox TTS deployment optimized for Apple Silicon M1 MacBook Air"
4. Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

**Option B: Via GitHub CLI**

```bash
# Install GitHub CLI if you don't have it
brew install gh

# Authenticate
gh auth login

# Create repository
gh repo create chatterbox-m1-project --public --source=. --remote=origin --push
```

### Step 7: Push to GitHub

If you created the repo via website:

```bash
# Add remote
git remote add origin https://github.com/YOUR-USERNAME/chatterbox-m1-project.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 8: Verify Upload

1. Visit your repository: https://github.com/mkoker/chatterbox-m1-project
2. Check that README.md displays properly
3. Verify files are present
4. Test clone from another location

## Repository Settings

### Recommended Settings

1. **About Section** (gear icon):
   - Description: "Production-ready Chatterbox TTS deployment for Apple Silicon M1"
   - Website: (optional)
   - Topics: `voice-cloning`, `text-to-speech`, `apple-silicon`, `m1`, `tts`, `chatterbox`, `pytorch`, `fastapi`

2. **Features**:
   - ✅ Issues
   - ✅ Projects (optional)
   - ✅ Wiki (optional)
   - ✅ Discussions (optional)

3. **Branch Protection** (Settings > Branches):
   - Protect `main` branch
   - Require pull request reviews
   - Require status checks

### Create Useful Labels

Go to Issues > Labels and add:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `apple-silicon` - Specific to M1/M2/M3
- `performance` - Performance improvements
- `compatibility` - Compatibility issues

## Adding a README Badge

Add status badges to your README:

```markdown
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Apple%20Silicon-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
```

## Repository Structure Best Practices

Your current structure is good. Consider adding:

```
chatterbox-m1-project/
├── .github/                # GitHub-specific files
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/          # GitHub Actions (optional)
│       └── tests.yml
├── docs/                   # Documentation
├── examples/              # Example code
├── scripts/               # Utility scripts
└── tests/                 # Test files (future)
```

## Maintaining Your Repository

### Regular Updates

```bash
# Make changes
git add .
git commit -m "feat: Add new voice profile feature"
git push

# Create a new release
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

### Handling Issues

1. Respond promptly to issues
2. Use labels to organize
3. Close resolved issues
4. Reference issues in commits: `fixes #42`

### Accepting Pull Requests

1. Review code changes
2. Test on M1 hardware if possible
3. Request changes if needed
4. Merge when ready
5. Thank contributors

## Security Considerations

### Files to NEVER Commit

- API keys or secrets
- Personal reference audio files
- Large model files (use Git LFS or download separately)
- Generated audio outputs
- Database files

### Check Before Pushing

```bash
# Search for potential secrets
git grep -i "api_key"
git grep -i "password"
git grep -i "secret"

# Review files being committed
git diff --cached
```

## Making It Discoverable

### README Improvements

- Add screenshots/GIFs of the web interface
- Include performance benchmarks
- Show code examples
- Link to live demo (if applicable)

### Promotion

- Share on relevant subreddits (r/MachineLearning, r/MacOS)
- Post on Twitter/X with relevant hashtags
- Add to awesome lists (awesome-tts, awesome-apple-silicon)
- Write a blog post about your experience

## Example First Issue

Create a welcoming first issue:

**Title**: "Welcome new contributors! Good first issues available"

**Body**:
```markdown
Thank you for your interest in contributing!

Here are some ways to get started:

- 📝 Improve documentation
- 🐛 Fix a bug from the issues list
- ✨ Add a new voice preset
- 🧪 Add test coverage
- 📱 Create integration examples

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Questions? Open an issue or discussion!
```

## Troubleshooting

**Issue**: Git is tracking large files  
**Fix**: Add to .gitignore and run `git rm --cached filename`

**Issue**: Accidentally committed secrets  
**Fix**: Remove from history with `git filter-branch` or BFG Repo-Cleaner

**Issue**: Want to start over  
**Fix**: Delete .git folder and re-initialize

## Next Steps

After publishing:

1. Star your own repository
2. Watch for issues and PRs
3. Set up GitHub Actions for automated testing (optional)
4. Create releases for major versions
5. Engage with users and contributors

---

**Your repository is now ready for the world!**

To update this guide in your repo, you can commit and push changes anytime:

```bash
git add GITHUB_GUIDE.md
git commit -m "docs: Update GitHub publishing guide"
git push
```