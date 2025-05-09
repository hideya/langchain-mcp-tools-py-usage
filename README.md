# MCP Tools Usage From LangChain / Example in Python [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/hideya/langchain-mcp-tools-py-usage/blob/main/LICENSE)

This simple [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
client demonstrates the use of MCP server tools by LangChain ReAct Agent.

It leverages a utility function `convert_mcp_to_langchain_tools()` from
[`langchain_mcp_tools`](https://pypi.org/project/langchain-mcp-tools/).  
This function handles parallel initialization of specified multiple MCP servers
and converts their available tools into a list of LangChain-compatible tools
([list[BaseTool]](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.base.BaseTool.html#langchain_core.tools.base.BaseTool)).

Anthropic's `claude-3-7-sonnet-latest` is used as the LLM.
For convenience, code for OpenAI's `o3-mini` is also included and commented out.

A bit more realistic (conversational) MCP Client is available
[here](https://github.com/hideya/mcp-client-langchain-py)

A typescript equivalent of this MCP client is available
[here](https://github.com/hideya/langchain-mcp-tools-ts-usage)

## Prerequisites

- Python 3.11+
- [optional] [`uv` (`uvx`)](https://docs.astral.sh/uv/getting-started/installation/)
  installed to run Python package-based MCP servers
- [optional] [npm 7+ (`npx`)](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
  to run Node.js package-based MCP servers
- API key from [Anthropic](https://console.anthropic.com/settings/keys)
  (or [OpenAI](https://platform.openai.com/api-keys))

## Usage

1. Install dependencies:
    ```bash
    make install
    ```

2. Setup API key:
    ```bash
    cp .env.template .env
    ```
    - Update `.env` as needed.
    - `.gitignore` is configured to ignore `.env`
      to prevent accidental commits of the credentials.

3. Run the app:
```bash
make start
```
It takes a while on the first run.
