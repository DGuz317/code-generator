"""Time sub‑agent implementation.

The agent demonstrates how a sub‑agent consumes a filtered MCP tool‑set
produced by :pymod:`src.multi_agent_fastmcp_adk.tools.mcp_client`. The
actual MCP call is currently a stub (see that module) – the purpose of this
file is to wire the pieces together so later development can replace the stub
with a real implementation.
"""

from __future__ import annotations

from typing import Any

from ..tools.mcp_client import get_time_toolset


def get_current_time() -> Any:
    """Return the current time using the MCP ``tell_time`` tool.

    The function obtains a filtered tool‑set that contains only the time‑related
    MCP tool (as configured in :pymod:`src.multi_agent_fastmcp_adk.config`). It
    then invokes the tool. Because the underlying tool is a stub, a
    ``RuntimeError`` will be raised until the MCP integration is completed.
    """

    toolset = get_time_toolset()
    # The filtered set contains exactly one entry.
    (_, tool) = next(iter(toolset.items()))
    return tool()


__all__ = ["get_current_time"]
