# Contributing to Exerset

Thanks for your interest in improving Exerset! This guide will help you contribute effectively.

## How to Report Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Title: Clear summary of the problem
   - Description: What you expected vs. what happened
   - Environment: OS, Python version, app version
   - Steps to reproduce: Exact steps to trigger the bug
   - Logs or screenshots: Any error messages or visual evidence

## How to Suggest Features

1. Check existing issues first
2. Create an issue with:
   - Title: Clear description of the feature
   - Motivation: Why this feature would be useful
   - Proposed behavior: How users would interact with it
   - Alternative approaches: Any workarounds or other solutions considered

## Development Setup

### Clone and Install

```bash
git clone https://github.com/drjosh/exerset.git
cd exerset
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```

### Code Style

- Follow PEP 8
- Use meaningful variable and function names
- Keep functions focused and small
- Add docstrings for public functions

### Testing

Before submitting a pull request:

1. Test on your platform (Windows/macOS/Linux)
2. Run the app: `python run.py`
3. Test core features:
   - Timer countdown
   - Exercise logging
   - History display
   - Tray interactions
4. If platform-specific: test on other platforms if possible

## Submitting Changes

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Commit with clear messages: `git commit -m "Add feature: clear description"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Create a Pull Request with:
   - Clear description of changes
   - Reference to related issues
   - Steps tested

## Pull Request Guidelines

- Keep changes focused and minimal
- Include any new dependencies in requirements.txt
- Update documentation if needed (README.md, INSTALL.md, etc.)
- Link related issues
- Be descriptive in commit messages

## Project Structure

Key files to understand before contributing:

- `src/exerset/main.py` - Application lifecycle and setup
- `src/exerset/ui/main_window.py` - Main UI layout and widgets
- `src/exerset/storage.py` - History persistence logic
- `src/exerset/timer_controller.py` - Timer and notification logic
- `build/build-*.sh` and `.ps1` - Release build automation

## Building Releases

If you're interested in building standalone apps:

See [build/BUILD.md](build/BUILD.md) for Windows/macOS build instructions.

## Code Review Process

Maintainers will review pull requests and may ask for changes. This is normal! We want to ensure:

- Code quality and style consistency
- No breaking changes
- Cross-platform compatibility
- Clear commit history

## Questions?

Open an issue for discussion or ask in pull request comments.

Thank you for contributing!
