Thank you for taking interest in this project.

Guidelines for contribution

- Keep changes small and focused. Open a branch named `feature/<short-desc>` or `fix/<short-desc>`.
- Add tests for any new behavior. Use `pytest`.
- Follow the existing project layout and typing hints.

Testing locally

1. Create a virtual environment and install dev dependencies:

   python -m venv .venv
   source .venv/bin/activate
   uv pip install -e .

2. Run tests:

   pytest -q

Code style and formatting

- This repo does not enforce a formatter, but please keep code readable and follow common Python conventions (PEP8).
