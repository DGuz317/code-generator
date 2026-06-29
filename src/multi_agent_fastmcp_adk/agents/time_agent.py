"""Time sub‑agent implementation using ADK.

This module defines a sub‑agent that wraps the MCP ``tell_time`` tool in an
ADK ``Agent`` instance. The agent can be routed to by a root agent in a multi‑
agent workflow.
"""

from __future__ import annotations

from typing import Any, Dict

# ADK Agent class – imported lazily to avoid hard dependency if the package is not installed.
try:
    from google.adk.agents.llm_agent import Agent  # type: ignore
except ImportError:  # pragma: no cover
    # Fallback stub for environments without the ADK package.
    class Agent:  # pylint: disable=too-few-public-methods
        def __init__(self, *_, **__):
            raise RuntimeError("google.adk is not installed in this environment")

from ..tools.mcp_client import get_time_toolset


def _mcp_time_tool(city: str) -> Dict[str, Any]:
    """Call the MCP ``tell_time`` tool for a given *city*.

    The underlying MCP client currently provides a stub implementation which
    raises ``RuntimeError`` until a real MCP server is wired up.
    """

    toolset = get_time_toolset()
    # The filtered set contains exactly one entry.
    (_, tool) = next(iter(toolset.items()))
    # The stub tool does not accept arguments, but we keep the signature to
    # match ADK's expectations.
    result = tool()
    return {"city": city, "time": result}

# Define the sub‑agent.
time_agent = Agent(
    model="ollama_chat/gpt-oss:20b",
    name="time_agent",
    description="Provides the current time via the MCP 'tell_time' tool.",
    instruction="Use the provided _mcp_time_tool to obtain the current time for a city.",
    tools=[_mcp_time_tool],
)

__all__ = ["time_agent"]
