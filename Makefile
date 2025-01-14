# NOTES: 
# - The command lines (recipe lines) must start with a TAB character.
# - Each command line runs in a separate shell.
.PHONY: install start build clean

.venv:
	uv venv

install: .venv
	uv pip install .

start:
	uv run src/example.py

build:
	uv build

clean:
	git clean -fdx
