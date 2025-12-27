"""
Worker agent node for executing individual tasks within the execution plan.
"""

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END

from models import WorkerTask
from prompts import WORKER_AGENT_SYSTEM_PROMPT
from tools import get_all_tools
from utils import get_llm


class WorkerAgentState(BaseModel):
    """
    State specific to the worker agent executing a single task.
    """

    messages: List[BaseMessage] = Field(
        default_factory=list,
        description="Conversation messages exchanged during task execution"
    )
    
    task: WorkerTask = Field(
        description="The specific worker task being executed"
    )
    
    final_result: str = Field(
        default="",
        description="Final result produced by the worker agent"
    )
    
    llm: Optional[ChatOpenAI] = Field(
        default=None,
        description="Language model used by the worker agent"
    )
    
    class Config:
        arbitrary_types_allowed = True


async def init_node(state: dict) -> dict:
    """
    Initialization node for setting up the worker agent state.
    """
    task = state["task"]
    print(f"      → Starting worker: {task.name}")
    tools = []
    if task.needs_web_search:
        tools = get_all_tools()
    state["llm"] = get_llm(temperature=task.temperature).bind_tools(tools)
    msg = await _create_prompt(state)
    state["messages"].extend(msg)
    state["iteration_count"] = 0
    state["tool_calls_count"] = 0
    return state

async def _create_prompt(state: dict) -> List[BaseMessage]:
    """Create the prompt for the worker agent based on the task."""
    task = state["task"]
    base_prompt = SystemMessage(content=WORKER_AGENT_SYSTEM_PROMPT)
    task_prompt = f"""
You are assigned the following task:

{task.detailed_task_outline}

Expected output format:
{task.expected_output}
"""
    return [base_prompt, HumanMessage(content=task_prompt)]

async def execute_task(state: dict) -> dict:
    """Execute the LLM and update state with the response"""
    import asyncio
    from openai import RateLimitError, APIError

    # Increment iteration count
    state["iteration_count"] = state.get("iteration_count", 0) + 1

    # Safety check: if too many iterations, force end
    MAX_ITERATIONS = 15
    if state["iteration_count"] > MAX_ITERATIONS:
        state["final_result"] = "Maximum iterations reached. Using accumulated information."
        return state

    # Retry logic for rate limits
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            response = await state["llm"].ainvoke(state["messages"])
            state["messages"].append(response)

            # If no tool calls, this is the final answer
            if not response.tool_calls:
                state["final_result"] = response.content

            return state
        except RateLimitError as e:
            if "Request too large" in str(e):
                # Token limit exceeded - summarize conversation
                state["final_result"] = "Response size limit exceeded. Unable to complete task with current context."
                return state
            elif attempt < max_retries - 1:
                # Rate limit - wait and retry
                await asyncio.sleep(retry_delay * (attempt + 1))
            else:
                # Max retries reached
                state["final_result"] = f"Rate limit error after {max_retries} attempts: {str(e)}"
                return state
        except APIError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                state["final_result"] = f"API error: {str(e)}"
                return state
        except Exception as e:
            # Unexpected error
            state["final_result"] = f"Unexpected error: {str(e)}"
            return state

    return state

async def should_continue(state: dict) -> Literal["tools", "end"]:
    """Route to tools if LLM made tool calls, otherwise end"""
    # Check iteration count first
    MAX_ITERATIONS = 15
    if state.get("iteration_count", 0) > MAX_ITERATIONS:
        print(f"        ⚠ Max iterations ({MAX_ITERATIONS}) reached")
        return "end"

    # Check tool call limit
    MAX_TOOL_CALLS = 10
    if state.get("tool_calls_count", 0) >= MAX_TOOL_CALLS:
        print(f"        ⚠ Max tool calls ({MAX_TOOL_CALLS}) reached")
        return "end"

    last_message = state["messages"][-1]

    # Check if we have tool calls
    tool_calls = getattr(last_message, 'tool_calls', None)

    # Make sure tool_calls is not None and not empty
    if tool_calls and len(tool_calls) > 0:
        return "tools"
    else:
        return "end"

async def execute_tools(state: dict) -> dict:
    """Custom tool execution node that properly handles tool calls and responses."""
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, 'tool_calls', [])

    if not tool_calls:
        return state

    # Get the tools
    tools = get_all_tools()
    tools_by_name = {tool.name: tool for tool in tools}

    # Track how many tool calls we're making
    num_calls = len(tool_calls)
    state["tool_calls_count"] = state.get("tool_calls_count", 0) + num_calls

    # Execute each tool call and create tool messages
    tool_messages = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        if tool_name in tools_by_name:
            try:
                # Execute the tool
                result = await tools_by_name[tool_name].ainvoke(tool_args)

                # Create a tool message with the result
                tool_message = ToolMessage(
                    content=str(result),
                    tool_call_id=tool_id
                )
                tool_messages.append(tool_message)
            except Exception as e:
                # Create an error tool message (only show errors)
                tool_message = ToolMessage(
                    content=f"Error executing {tool_name}: {str(e)}",
                    tool_call_id=tool_id
                )
                tool_messages.append(tool_message)

    # Add all tool messages to the state
    state["messages"].extend(tool_messages)
    return state

def create_worker_graph(task: WorkerTask):
    """Create the subgraph for the worker agent execution."""
    from typing import TypedDict

    # Define state as a TypedDict instead of Pydantic model
    class WorkerState(TypedDict):
        task: WorkerTask
        messages: list
        final_result: str
        llm: Optional[ChatOpenAI]
        iteration_count: int
        tool_calls_count: int

    worker = StateGraph(WorkerState)
    worker.add_node("init", init_node)
    worker.add_node("execute", execute_task)

    # Add custom tool execution node if task needs web search
    if task.needs_web_search:
        worker.add_node("tools", execute_tools)

    worker.set_entry_point("init")
    worker.add_edge("init", "execute")

    if task.needs_web_search:
        worker.add_conditional_edges("execute", should_continue, {"tools": "tools", "end": END})
        worker.add_edge("tools", "execute")
    else:
        # No tools, always end after execute
        worker.add_edge("execute", END)

    # Compile with increased recursion limit
    return worker.compile(checkpointer=None, interrupt_before=None, interrupt_after=None, debug=False)