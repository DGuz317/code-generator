# Client Request: ADK Multi-Agent System with FastMCP Tools and Local Ollama LLM

## 1. Objective

Build a Python-based multi-agent system using Google Agent Development Kit (ADK). The system must connect to an existing FastMCP server where the tools are hosted. The agent application must use a local Ollama model for LLM inference, specifically `gpt-oss:20b`.

The system must include:

- One root orchestrator agent that decides which sub-agent should handle each user request.
- One `tell_time` sub-agent responsible only for time-related requests.
- One `calculator` sub-agent responsible only for arithmetic or numeric calculation requests.
- MCP-based tool access through the FastMCP server, not local inline tool definitions inside the agents.

The implementation must not place all code in one file. It must be organized into a maintainable multi-file project structure.

## 2. Reference Framework Requirements

Use the official ADK 2.x.x documentation as the implementation reference, especially for:

- ADK multi-agent / collaborative workflow patterns.
- Parent agent and sub-agent hierarchy.
- Agent delegation from an orchestrator to specialized sub-agents.
- MCP tool integration through ADK `McpToolset` / MCP client support.
- Local model usage through LiteLLM and Ollama.

The implementation should follow ADK conventions instead of creating a custom orchestration framework from scratch.

## 3. LLM Inference Requirement

The LLM must run locally through Ollama.

Required model:

```env
ADK_MODEL=ollama_chat/gpt-oss:20b
OLLAMA_API_BASE=http://localhost:11434
```

Important implementation constraints:

- Use ADK's LiteLLM integration for the local Ollama model.
- Use the `ollama_chat` provider prefix, not plain `ollama`, to avoid incorrect tool-calling behavior.
- The app must assume Ollama is running locally before the agent process starts.
- The project should expose the model name through configuration, not hard-code it throughout the codebase.

## 4. MCP / FastMCP Requirement

The tools must live in the FastMCP server.

The ADK application should connect to the FastMCP server as an MCP client and expose the MCP tools to the correct sub-agents.

Expected MCP tools:

- A time tool, for example: `tell_time`, `get_current_time`, or equivalent.
- A calculator tool, for example: `calculate`, `calculate_number`, or equivalent.

The exact MCP tool names may be configured in one place if the FastMCP server uses different names.

The implementation must support one of these MCP connection styles, based on the existing FastMCP server setup:

- `stdio`, if the ADK app starts the MCP server as a local process.
- `sse`, if the FastMCP server exposes a Server-Sent Events endpoint.
- `streamable_http`, if the FastMCP server exposes streamable HTTP transport.

Configuration should be handled through environment variables.

Example configuration:

```env
MCP_TRANSPORT=stdio
MCP_SERVER_COMMAND=python
MCP_SERVER_ARGS=server.py
MCP_SERVER_URL=http://localhost:8000/mcp
MCP_TIME_TOOL_NAME=tell_time
MCP_CALCULATOR_TOOL_NAME=calculate_number
```

## 5. Required Agent Design

### 5.1 Root Orchestrator Agent

Name: `orchestrator_agent`

Responsibilities:

- Receive the user's natural-language request.
- Decide whether the request is time-related or calculation-related.
- Delegate the request to the correct sub-agent.
- Return the final answer to the user.
- Avoid directly calling MCP tools unless explicitly required by ADK routing behavior.

The orchestrator should not contain the full logic for time lookup or arithmetic calculation. Its main responsibility is delegation.

### 5.2 Time Sub-Agent

Name: `time_agent`

Responsibilities:

- Handle requests about the current time.
- Use only the time-related MCP tool from the FastMCP server.
- Return concise time answers.
- Refuse or defer non-time tasks back to the orchestrator.

Example supported requests:

- `What time is it?`
- `Tell me the current time.`
- `What is the time in Ho Chi Minh City?`

### 5.3 Calculator Sub-Agent

Name: `calculator_agent`

Responsibilities:

- Handle arithmetic and numeric calculation requests.
- Use only the calculator-related MCP tool from the FastMCP server.
- Return the calculated result and, when useful, a short explanation.
- Refuse or defer non-calculation tasks back to the orchestrator.

Example supported requests:

- `What is 24 * 18?`
- `Calculate 12.5% of 800.`
- `What is (15 + 9) / 3?`

## 6. Required Project Structure

Use a multi-file structure similar to the following:

```text
multi-agent-fastmcp-adk/
├── client-request.md
├── README.md
├── pyproject.toml
├── .env.example
├── src/
│   └── multi_agent_fastmcp_adk/
│       ├── __init__.py
│       ├── config.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── root_agent.py
│       │   ├── time_agent.py
│       │   └── calculator_agent.py
│       ├── tools/
│       │   ├── __init__.py
│       │   └── mcp_client.py
│       └── runners/
│           ├── __init__.py
│           └── cli.py
└── tests/
    ├── test_agent_routing.py
    ├── test_mcp_tool_config.py
    └── test_basic_requests.py
```

Do not implement the entire system in a single `agent.py` file.

## 7. Suggested File Responsibilities

### `config.py`

- Load environment variables.
- Define the Ollama model configuration.
- Define MCP transport settings.
- Define MCP tool names.

### `tools/mcp_client.py`

- Build reusable MCP toolsets for ADK agents.
- Apply tool filtering so each sub-agent only receives the MCP tools it is allowed to use.
- Centralize MCP connection setup.

### `agents/time_agent.py`

- Define the ADK time sub-agent.
- Attach only the time MCP toolset.
- Use the local Ollama model configuration.

### `agents/calculator_agent.py`

- Define the ADK calculator sub-agent.
- Attach only the calculator MCP toolset.
- Use the local Ollama model configuration.

### `agents/root_agent.py`

- Define the orchestrator agent.
- Register `time_agent` and `calculator_agent` as sub-agents.
- Include routing/delegation instructions.

### `runners/cli.py`

- Provide a simple local CLI runner for manual testing.
- Keep runtime code separate from agent definitions.

## 8. Expected Runtime Flow

### Time request flow

```text
User request
  -> orchestrator_agent
  -> delegates to time_agent
  -> time_agent calls FastMCP time tool through ADK MCP toolset
  -> time_agent returns result
  -> orchestrator_agent returns final response
```

### Calculation request flow

```text
User request
  -> orchestrator_agent
  -> delegates to calculator_agent
  -> calculator_agent calls FastMCP calculator tool through ADK MCP toolset
  -> calculator_agent returns result
  -> orchestrator_agent returns final response
```

## 9. Implementation Constraints

- Use Python.
- Use Google ADK for agent creation and orchestration.
- Use LiteLLM through ADK for Ollama local inference.
- Use `ollama_chat/gpt-oss:20b` as the default model.
- Use FastMCP as the MCP server where tools are exposed.
- Use ADK MCP integration rather than manually calling HTTP endpoints from inside the agents.
- Keep agent definitions, MCP setup, configuration, and runner code in separate files.
- Keep sub-agent tool access scoped by responsibility.
- Avoid giving the orchestrator unnecessary direct tool access.
- Avoid implementing time and calculator logic locally if those tools already exist in the FastMCP server.

## 10. Testing Requirements

Add tests or manual test scripts that verify:

- The orchestrator delegates time requests to `time_agent`.
- The orchestrator delegates calculation requests to `calculator_agent`.
- `time_agent` only has access to the time MCP tool.
- `calculator_agent` only has access to the calculator MCP tool.
- The system uses the configured Ollama model.
- The app fails clearly if Ollama is not running.
- The app fails clearly if the FastMCP server is unavailable.

Example test prompts:

```text
What time is it?
Tell me the current time in Ho Chi Minh City.
What is 25 * 16?
Calculate (12 + 8) / 5.
```

## 11. Acceptance Criteria

The implementation is complete when:

- The project uses a multi-file structure.
- The root orchestrator agent can route user requests to the correct sub-agent.
- The time sub-agent can call the FastMCP time tool and return a valid answer.
- The calculator sub-agent can call the FastMCP calculator tool and return a valid answer.
- The system uses Ollama with `gpt-oss:20b` through ADK LiteLLM configuration.
- The MCP connection settings are configurable through environment variables.
- The README explains how to run Ollama, start or connect to the FastMCP server, and launch the ADK agent.
- The implementation follows ADK multi-agent and MCP integration patterns.

## 12. Out of Scope

The following are not required unless requested separately:

- Building a web UI.
- Adding database persistence.
- Adding authentication.
- Creating new MCP tools if the FastMCP server already provides them.
- Deploying the system to cloud infrastructure.
- Supporting unrelated tools beyond time and calculator.

## 13. Deliverables

The developer should provide:

- Full project source code using the multi-file structure above.
- `.env.example` with required configuration keys.
- README with setup and run instructions.
- Basic tests or documented manual verification steps.
- Clear notes for how the ADK app connects to the FastMCP server.

