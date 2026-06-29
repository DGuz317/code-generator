"""MCP client helper for the FastMCP ADK.

This module centralises the creation of tool‑sets that agents can use to call
remote MCP tools. It reads configuration from :pymod:`src.multi_agent_fastmcp_adk.config`
and currently implements a very small stub that can be expanded later.
"""

from __future__ import annotations

import os
import subprocess
from typing import Callable, Dict

from .. import config

# ---------------------------------------------------------------------------
# Internal connection handling (stubbed)
# ---------------------------------------------------------------------------

def _ensure_transport() -> None:
    """Validate that the selected transport is supported.

    At the moment only ``stdio`` is implemented. If a different transport is
    configured we raise a clear ``RuntimeError`` so the caller knows the
    limitation.
    """
    if config.MCP_TRANSPORT != "stdio":
        raise RuntimeError(
            f"Unsupported MCP transport '{config.MCP_TRANSPORT}'. Only 'stdio' is supported."
        )

# In a full implementation this would start the FastMCP server process and
# keep a handle to its stdin/stdout. For now we merely verify the transport.

def _connect() -> None:
    _ensure_transport()
    # Placeholder for real connection logic.
    return None

# ---------------------------------------------------------------------------
# Stub tool function generator
# ---------------------------------------------------------------------------

def _stub_tool(name: str) -> Callable[..., str]:
    """Return a callable that mimics an MCP tool.

    The callable raises ``RuntimeError`` indicating that the real MCP call is
    not wired up. This makes failure modes obvious during development while
    keeping the API surface stable.
    """

    def _inner(*_args, **_kwargs) -> str:
        raise RuntimeError(
            f"MCP tool '{name}' is a stub – real implementation not provided."
        )

    return _inner

# ---------------------------------------------------------------------------
# Public helper factories
# ---------------------------------------------------------------------------

def get_time_toolset() -> Dict[str, Callable[..., str]]:
    """Return a filtered tool‑set containing only the time‑related MCP tool.

    The dictionary maps the configured tool name (default ``tell_time``) to a
    stub callable. Real logic should replace the stub with a function that
    communicates with the MCP server.
    """

    _connect()
    return {config.MCP_TIME_TOOL_NAME: _stub_tool(config.MCP_TIME_TOOL_NAME)}


def get_calculator_toolset() -> Dict[str, Callable[..., str]]:
    """Return a filtered tool‑set containing only the calculator MCP tool.

    Mirrors :func:`get_time_toolset` but for the calculator tool.
    """

    _connect()
    return {config.MCP_CALCULATOR_TOOL_NAME: _stub_tool(config.MCP_CALCULATOR_TOOL_NAME)}


__all__ = ["get_time_toolset", "get_calculator_toolset"]
