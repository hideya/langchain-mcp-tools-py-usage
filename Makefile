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

update-lib:
	uv remove langchain-mcp-tools && uv add langchain-mcp-tools

run-sse-auth-test-client: install
	uv pip install -e ".[dev]"
	uv run src/sse-auth-test-client.py --no-server

run-sse-auth-test-server: install
	uv pip install -e ".[dev]"
	uv run src/sse-auth-test-server.py

clean:
	git clean -fdxn -e .env
	@read -p 'OK?'
	git clean -fdx -e .env
