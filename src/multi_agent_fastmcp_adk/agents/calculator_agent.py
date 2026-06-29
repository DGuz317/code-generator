"""Calculator sub‑agent implementation using ADK.

This module defines a sub‑agent that wraps the MCP ``calculate_number`` tool in an
ADK ``Agent`` instance. The stub MCP client currently raises a ``RuntimeError``
until a real MCP server is connected.
"""

from __future__ import annotations

from typing import Any, Dict

# Import ADK Agent lazily; provide a clear error if the package is missing.
try:
    from google.adk.agents.llm_agent import Agent  # type: ignore
except ImportError:  # pragma: no cover
    class Agent:  # pylint: disable=too-few-public-methods
        def __init__(self, *_, **__):
            raise RuntimeError("google.adk is not installed in this environment")

from ..tools.mcp_client import get_calculator_toolset


def _mcp_calculator_tool(expression: str) -> Dict[str, Any]:
    """Call the MCP ``calculate_number`` tool for *expression*.

    The underlying MCP client provides a stub implementation that raises a
    ``RuntimeError``. The function keeps the ADK‑expected signature so the
    agent can be wired into a workflow immediately.
    """

    toolset = get_calculator_toolset()
    # The filtered set contains exactly one entry.
    (_, tool) = next(iter(toolset.items()))
    result = tool()
    return {"expression": expression, "result": result}

# Define the calculator sub‑agent.
calculator_agent = Agent(
    model="ollama_chat/gpt-oss:20b",
    name="calculator_agent",
    description="Performs arithmetic calculations via the MCP 'calculate_number' tool.",
    instruction="Use the provided _mcp_calculator_tool to evaluate arithmetic expressions.",
    tools=[_mcp_calculator_tool],
)

__all__ = ["calculator_agent"]
