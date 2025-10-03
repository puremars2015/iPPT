# Repository Guidelines

## Project Structure & Module Organization
Keep the CLI entrypoint `ppt_agent.py` in the repository root; it orchestrates the Template Analyzer, Outline Manager, Layout Matcher, Content Generator, and Slide Generator stages described in `README.md`. Place implementation modules in `agents/` with one submodule per stage (for example, `agents/template_analyzer.py`). Shared utilities (I/O, logging, validation) belong in `core/`, while configuration defaults go in `config/settings.py`. Templates (`.pptx`) sit under `templates/`; never edit them in place, create a new file when changes are required. Generated presentations and derived images are written to `output/` and should be gitignored. Tests mirror the source layout under `tests/`, for example `tests/agents/test_layout_matcher.py`.

## Build, Test, and Development Commands
Create a virtual environment before installing dependencies: `python -m venv .venv` followed by `.venv\Scripts\activate`. Install runtime and tooling packages with `pip install -r requirements.txt`. Use `python ppt_agent.py --help` to inspect CLI options and `python ppt_agent.py --template templates/company_template.pptx --outline "<sample>"` for manual smoke checks. Run the full test suite with `pytest`. Validate slide templates with `python tools/inspect_template.py templates/company_template.pptx` before committing new assets.

## Coding Style & Naming Conventions
Target Python 3.11+. Format code with `black` (line length 100) and lint with `ruff`. Prefer descriptive module level names such as `TemplateAnalyzer` and `OutlineManager`; use snake_case for functions, methods, and variables. CLI options use kebab-case long flags such as `--max-slides`. Keep functions under 40 lines and extract helpers when orchestrating multiple pipeline phases.

## Testing Guidelines
Cover every agent stage with unit tests that stub external I/O. Name tests following `test_<module>_<behavior>` and keep fixtures in `tests/fixtures/`. Write integration tests that exercise a minimal template against a short outline; ensure generated decks retain placeholders. Aim for at least 80 percent line coverage, and update `coverage.xml` when thresholds change.

## Commit & Pull Request Guidelines
The repository lacks historical commits, so adopt Conventional Commits (`feat:`, `fix:`, `chore:`) to communicate intent. Reference relevant issues in the commit body. Pull requests must include: purpose summary, checklist of validation steps (lint, tests, manual deck preview), screenshots or GIFs for template updates, and notes on backward compatibility. Request review from another agent before merging.

## Agent Handoff Notes
Always document template or CLI contract changes in `README.md` and announce breaking API shifts in the PR description. Attach sample outputs in `output/samples/` for QA to reference.
