# SuperClaude Copilot Instructions

Use these rules when assisting in this repository.

## Environment and commands
- Use `uv` for all Python operations.
- Prefer Make targets for standard workflows:
  - `make install`
  - `make lint`
  - `make test`
  - `make verify`
  - `make copilot-check`

## Task workflow
- Start by reading `AGENTS.md` and `CLAUDE.md`.
- Keep changes minimal and scoped to the request.
- Reuse existing patterns in `src/superclaude/` and existing tests in `tests/`.
- When changing CLI behavior, validate with:
  - `uv run superclaude --help`
  - `uv run superclaude version`
  - `uv run superclaude install --list`
  - `uv run superclaude mcp --list`

## Testing expectations
- Run lint and tests before concluding:
  - `make lint`
  - `make test`
- For command wiring updates, add or update unit tests under `tests/unit/`.

## Safety and consistency
- Do not introduce new dependencies unless required.
- Do not modify unrelated files.
- Follow existing naming and style conventions.
