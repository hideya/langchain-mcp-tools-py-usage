# NOTES: 
# - The command lines (recipe lines) must start with a TAB character.
# - Each command line runs in a separate shell.
.PHONY: install start clean

.venv:
	uv venv

install: .venv
	uv pip install .

start:
	uv run src/example.py

clean:
	git clean -fdxn -e .env
	@read -p 'OK?'
	git clean -fdx -e .env
