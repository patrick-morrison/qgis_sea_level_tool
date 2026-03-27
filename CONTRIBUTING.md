# Contributing to Sea Level Tool

Thank you for your interest in contributing to the Sea Level Tool QGIS plugin.

## Reporting Bugs

Please report bugs via the [GitHub issue tracker](https://github.com/patrick-morrison/qgis_sea_level_tool/issues).

When reporting a bug, please include:
- QGIS version (Help > About)
- Operating system and version
- Steps to reproduce the problem
- What you expected to happen vs what actually happened
- Any error messages shown in the QGIS Python console (Plugins > Python Console)

## Suggesting Features

Feature requests are welcome via the issue tracker. Please describe the use case and how the feature would benefit users.

## Contributing Code

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/patrick-morrison/qgis_sea_level_tool.git
   ```

2. Install the plugin into QGIS by copying (or symlinking) the repository directory into your QGIS plugins folder:
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
   - Windows: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`

3. Enable the plugin in QGIS (Plugins > Manage and Install Plugins).

4. Compile Qt resources before testing:
   ```bash
   make compile
   ```

### Running Tests

Tests require a QGIS Python environment. With QGIS installed:

```bash
make test
```

Please ensure all existing tests pass before submitting a pull request.

### Submitting a Pull Request

1. Fork the repository on GitHub.
2. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes, following the existing code style (PEP 8).
4. Add or update tests as appropriate.
5. Run the test suite and confirm it passes.
6. Commit with a clear message describing the change.
7. Open a pull request against the `main` branch with a description of what was changed and why.

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Run `make pylint` and `make pep8` to check for style issues before submitting.
- Avoid introducing new dependencies where possible.

## Questions

For questions about using the plugin, please open a GitHub issue with the `question` label.
