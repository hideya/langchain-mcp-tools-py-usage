# NOTES: 
# - The command lines (recipe lines) must start with a TAB character.
# - Each command line runs in a separate shell.
.PHONY: clean install start start-v start-h build test clean

.venv:
	uv venv

install: .venv
	uv pip install .

start:
	uv run src/cli_chat.py

start-v:
	uv run src/cli_chat.py -v

start-h:
	uv run src/cli_chat.py -h

build:
	uv build

test:
	pytest tests/ -v

clean:
	rm -rf \
		.venv \
		__pycache__ \
		*/__pycache__ \
		build/ dist/ \
		*.egg-info \
		.mypy_cache \
		.pytest_cache \
		src/*.egg-info
