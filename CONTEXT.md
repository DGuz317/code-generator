# Project Context

- **MCP Transport Style**: `stdio` – the ADK application will start the FastMCP server as a local process and communicate via standard I/O streams.
- **MCP Time Tool Name**: `tell_time` – the name of the time‑related tool exposed by FastMCP, provided via the `MCP_TIME_TOOL_NAME` environment variable.
- **MCP Calculator Tool Name**: `calculate_number` – the name of the calculator tool exposed by FastMCP, provided via the `MCP_CALCULATOR_TOOL_NAME` environment variable.
- **Intent Detection**: Delegation decisions are made by prompting the LLM to classify the user request (model‑based intent detection).
- **MCP Tool Retry Policy**: Calls are retried up to a configurable number of times, defaulting to the value of the `MCP_TOOL_RETRY_COUNT` environment variable. If all retries fail, a clear error message is propagated to the user.
- **Configuration Access Pattern**: All configuration values (model name, MCP settings, retry count, etc.) are read directly with `os.getenv`; no typed settings objects are used.
- **Dependency Management**: The project uses **Poetry** for dependency declaration (`pyproject.toml`) and **uv** for fast installation of packages.
