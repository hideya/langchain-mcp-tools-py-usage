# Simple MCP Client Using LangChain / Python [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/hideya/langchain-mcp-tools-py-usage/blob/main/LICENSE)

This simple [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
client demonstrates MCP server invocations by LangChain ReAct Agent.

It leverages a utility function `convert_mcp_to_langchain_tools()` from
[`langchain_mcp_tools`](https://pypi.org/project/langchain-mcp-tools/).  
This function handles parallel initialization of specified multiple MCP servers
and converts their available tools into a list of
[LangChain-compatible tools](https://js.langchain.com/docs/how_to/tool_calling/).

Anthropic's `claude-3-5-haiku-latest` is used as the LLM.  
For convenience, code for OpenAI's `gpt-4o-mini` is also included and commented out.

A typescript version of this MCP client is available
[here](https://github.com/hideya/langchain-mcp-tools-ts-usage)

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) installation
- `ANTHROPIC_API_KEY` - get one from [Anthropic](https://console.anthropic.com/settings/keys)  
  If you switch to OpenAI's LLM, get `OPENAI_API_KEY` from [OpenAI](https://platform.openai.com/api-keys)

## Usage
1. Install dependencies:
    ```bash
    make install
    ```

2. Setup API keys:
    ```bash
    export ANTHROPIC_API_KEY=sk-ant-api...
    # export OPENAI_API_KEY=sk-proj-...
    ```

3. Run the app:
```bash
make start
```
