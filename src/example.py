# Standard library imports
import asyncio
import logging
import os
import socket
import subprocess
import sys
import time
from contextlib import ExitStack
from typing import (
    Any,
)

# Third-party imports
try:
    from dotenv import load_dotenv
    from langchain.chat_models import init_chat_model
    from langchain.schema import HumanMessage
    from langgraph.prebuilt import create_react_agent
except ImportError as e:
    print(f"\nError: Required package not found: {e}")
    print("Please ensure all required packages are installed\n")
    sys.exit(1)

# Local application imports
from langchain_mcp_tools import (
    convert_mcp_to_langchain_tools,
    McpServersConfig,
)

# A very simple logger
def init_logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,  # logging.DEBUG,
        format="\x1b[90m[%(levelname)s]\x1b[0m %(message)s"
    )
    return logging.getLogger()


async def run() -> None:
    # Be sure to set ANTHROPIC_API_KEY and/or OPENAI_API_KEY as needed
    load_dotenv()

    # If you are interested in testing the SSE/WS server connection,
    # uncomment one of the following code snippets and one of the
    # appropriate "weather" server configurations, while commenting
    # out the one for the stdio server

    # # Run a test SSE MCP server on the local machine
    # sse_server_process, sse_server_port = start_remote_mcp_server_locally(
    #     "SSE",  "npx -y @h1deya/mcp-server-weather")

    # # Run a test Websocket MCP server on the local machine
    # ws_server_process, ws_server_port = start_remote_mcp_server_locally(
    #     "WS",  "npx -y @h1deya/mcp-server-weather")

    try:
        mcp_servers: McpServersConfig = {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "."  # path to a directory to allow access to
                ],
                # "cwd": "/tmp"  # the working dir to be use by the server
            },

            "fetch": {
                "command": "uvx",
                "args": [
                    "mcp-server-fetch"
                ]
            },

            "weather": {
                "command": "npx",
                "args": [
                    "-y",
                    "@h1deya/mcp-server-weather"
                ]
            },

            # # Auto-detection example: This will try Streamable HTTP first, then fallback to SSE
            # "weather": {
            #     "url": f"http://localhost:{sse_server_port}/sse"
            # },

            # "weather": {
            #     "url": f"http://localhost:{sse_server_port}/sse",
            #     "transport": "sse"  # Force SSE
            #     # "type": "sse"  # This also works instead of the above
            # },

            # "weather": {
            #     "url": f"ws://localhost:{ws_server_port}/message",
            #     # optionally `"transport": "ws"` or `"type": "ws"`
            # },

            # # Example of authentication via Authorization header
            # # https://github.com/github/github-mcp-server?tab=readme-ov-file#remote-github-mcp-server
            # "github": {
            #     # To avoid auto protocol fallback, specify the protocol explicitly when using authentication
            #     "type": "http",
            #     # "__pre_validate_authentication": False,
            #     "url": "https://api.githubcopilot.com/mcp/",
            #     "headers": {
            #         "Authorization": f"Bearer {os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN', '')}"
            #     }
            # },
        }

        # If you are interested in MCP server's stderr redirection,
        # uncomment the following code snippets.

        # # Set a file-like object to which MCP server's stderr is redirected
        # log_file_exit_stack = ExitStack()
        # for server_name in mcp_servers:
        #     server_config = mcp_servers[server_name]
        #     # Skip URL-based servers (no command)
        #     if "command" not in server_config:
        #         continue
        #     log_path = f"mcp-server-{server_name}.log"
        #     log_file = open(log_path, "w")
        #     server_config["errlog"] = log_file
        #     log_file_exit_stack.callback(log_file.close)

        tools, cleanup = await convert_mcp_to_langchain_tools(
            mcp_servers,
            # optional: defaults to the module logger if not specified.
            # Fallback to a pre-configured logger if no root handlers exist.
            init_logger()
        )

        ### https://docs.anthropic.com/en/docs/about-claude/pricing
        ### https://console.anthropic.com/settings/billing
        # llm = init_chat_model("anthropic:claude-3-5-haiku-latest")
        # llm = init_chat_model("anthropic:claude-sonnet-4-0")
        
        ### https://platform.openai.com/docs/pricing
        ### https://platform.openai.com/settings/organization/billing/overview
        # llm = init_chat_model("openai:gpt-4o-mini")
        # llm = init_chat_model("openai:o4-mini")
        
        ### https://ai.google.dev/gemini-api/docs/pricing
        ### https://console.cloud.google.com/billing
        llm = init_chat_model("google_genai:gemini-2.0-flash")
        # llm = init_chat_model("google_genai:gemini-1.5-pro")

        agent = create_react_agent(
            llm,
            tools
        )

        # query = "Read the news headlines on bbc.com"
        # query = "Read and briefly summarize the LICENSE file"
        query = "Are there any weather alerts in California?"

        print("\x1b[33m")  # color to yellow
        print(query)
        print("\x1b[0m")   # reset the color

        messages = [HumanMessage(content=query)]

        result = await agent.ainvoke({"messages": messages})

        # the last message should be an AIMessage
        response = result["messages"][-1].content

        print("\x1b[36m")  # color to cyan
        print(response)
        print("\x1b[0m")   # reset the color

    finally:
        if "cleanup" in locals():
            await cleanup()

        # the following only needed when testing the `errlog` key
        if "log_file_exit_stack" in locals():
            log_file_exit_stack.close()

        # the followings only needed when testing the `url` key
        if "sse_server_process" in locals():
            sse_server_process.terminate()
        if "ws_server_process" in locals():
            ws_server_process.terminate()


# The following only needed when testing the SSE/WS MCP server connection
def start_remote_mcp_server_locally(
        transport_type, mcp_server_run_command, wait_time=2):
    """
    Start an MCP server process via supergateway with the specified transport
    type.  Supergateway runs MCP stdio-based servers over SSE or WebSockets
    and is used here to run local SSE/WS servers for connection testing.
    Ref: https://github.com/supercorp-ai/supergateway

    Args:
        transport_type (str): The transport type, either 'sse' or 'ws'
        mcp_server_package (str): The NPM package name for the MCP server
        wait_time (int): Time to wait for the server to start listening on its
        port

    Returns:
        tuple: (server_process, server_port)
    """
    def find_free_port():
        """Find and return a free port on localhost."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))  # Bind to a free port provided by the system
            return s.getsockname()[1]  # Return the port number assigned

    server_port = find_free_port()

    # Base command common to both server types
    command = [
        "npx",
        "-y",
        "supergateway",
        "--stdio",
        mcp_server_run_command,
        "--port", str(server_port),
    ]

    # Add transport-specific arguments
    if transport_type.lower() == 'sse':
        command.extend([
            "--baseUrl", f"http://localhost:{server_port}",
            "--ssePath", "/sse",
            "--messagePath", "/message"
        ])
    elif transport_type.lower() == 'ws':
        command.extend([
            "--outputTransport", "ws",
            "--messagePath", "/message"
        ])
    else:
        raise ValueError(f"Unsupported transport type: {transport_type}")

    # Start the server process
    server_process = subprocess.Popen(
        command,
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True
    )

    print(f"Started {transport_type.upper()} MCP Server Process with PID:"
          f" {server_process.pid}")
    time.sleep(wait_time)  # wait until the server starts listening on the port

    return server_process, server_port


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
