"""Configuration module for the multi‑agent FastMCP ADK project.

All required settings are read from environment variables using ``os.getenv``.
No typed settings objects are introduced – the values are accessed directly by
importing ``config`` wherever they are needed.

Required variables (with sensible defaults where appropriate):

* ``MCP_TRANSPORT`` – transport style for the FastMCP server (default ``stdio``).
* ``MCP_TIME_TOOL_NAME`` – name of the time‑related MCP tool (default
  ``tell_time``).
* ``MCP_CALCULATOR_TOOL_NAME`` – name of the calculator MCP tool (default
  ``calculate_number``).
* ``MCP_TOOL_RETRY_COUNT`` – number of retry attempts for MCP calls
  (default ``3``).
* ``ADK_MODEL`` – Ollama model identifier (default
  ``ollama_chat/gpt-oss:20b``).
* ``OLLAMA_API_BASE`` – base URL for the local Ollama server (default
  ``http://localhost:11434``).

If a required variable is missing, ``RuntimeError`` is raised with a clear
message so the application fails fast.
"""

import os

def _required(name: str, default: str | None = None) -> str:
    """Return the environment variable ``name`` or raise if missing.

    ``default`` is used only for optional settings; for required settings it
    should be ``None``.
    """
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

# Transport style – only ``stdio`` is currently supported in this project.
MCP_TRANSPORT = _required("MCP_TRANSPORT", "stdio")

# Tool names – configurable in case the FastMCP server uses different names.
MCP_TIME_TOOL_NAME = _required("MCP_TIME_TOOL_NAME", "tell_time")
MCP_CALCULATOR_TOOL_NAME = _required("MCP_CALCULATOR_TOOL_NAME", "calculate_number")

# Retry policy for MCP calls.
MCP_TOOL_RETRY_COUNT = int(_required("MCP_TOOL_RETRY_COUNT", "3"))

# Ollama model configuration.
ADK_MODEL = _required("ADK_MODEL", "ollama_chat/gpt-oss:20b")
OLLAMA_API_BASE = _required("OLLAMA_API_BASE", "http://localhost:11434")

__all__ = [
    "MCP_TRANSPORT",
    "MCP_TIME_TOOL_NAME",
    "MCP_CALCULATOR_TOOL_NAME",
    "MCP_TOOL_RETRY_COUNT",
    "ADK_MODEL",
    "OLLAMA_API_BASE",
]
