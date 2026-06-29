"""Root coordinator agent for the FastMCP ADK example.

This agent demonstrates a simple collaborative workflow:
* Directly responds to greetings ("hello", "goodbye").
* Delegates time‑related queries to ``time_agent``.
* Delegates arithmetic queries to ``calculator_agent``.

The sub‑agents are implemented using the same ADK pattern and expose a single
tool each. ``root_agent`` lists them in ``sub_agents`` so the ADK runtime can
automatically transfer control when the LLM decides a sub‑agent is needed.
"""

from __future__ import annotations

# ADK import with graceful fallback if the library is not installed.
try:
    from google.adk.agents.llm_agent import Agent  # type: ignore
except ImportError:  # pragma: no cover
    class Agent:  # pylint: disable=too-few-public-methods
        def __init__(self, *_, **__):
            raise RuntimeError("google.adk is not installed in this environment")

# Import the sub‑agents defined in this package.
from .time_agent import time_agent
from .calculator_agent import calculator_agent

# Define the coordinator (root) agent.
root_agent = Agent(
    model="ollama_chat/gpt-oss:20b",
    name="root_agent",
    description="Handles greetings and routes time or calculator requests to sub‑agents.",
    instruction=(
        "You are a friendly coordinator. If the user says 'hello' or 'goodbye' respond "
        "directly. For any request about the current time, delegate to the "
        "'time_agent' sub‑agent. For arithmetic calculations, delegate to the "
        "'calculator_agent' sub‑agent. Use the provided tools of each sub‑agent "
        "to fulfil the request."
    ),
    sub_agents=[time_agent, calculator_agent],
)

__all__ = ["root_agent"]
