"""
Main research agent graph that orchestrates the multi-agent research system.
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from models import AgentState
from nodes.planning import planning_node
from nodes.execution import execution_node
from nodes.evaluation import evaluation_node
from nodes.synthesis import synthesis_node


def should_continue_after_planning(state: AgentState) -> Literal["execute", "end"]:
    """
    Routing function after planning.
    - If planning failed, end the graph
    - Otherwise, proceed to execution
    """
    if state.status == "failed":
        return "end"
    return "execute"


def should_continue_after_execution(state: AgentState) -> Literal["evaluate", "end"]:
    """
    Routing function after execution.
    - If execution failed, end the graph
    - Otherwise, proceed to evaluation
    """
    if state.status == "failed":
        return "end"
    return "evaluate"


def should_continue_after_evaluation(state: AgentState) -> Literal["synthesize", "plan", "end"]:
    """
    Routing function after evaluation.
    - If evaluation determines research is complete (ready_for_synthesis), go to synthesis
    - If more research is needed, go back to planning
    - If evaluation failed, end the graph
    """
    if state.status == "failed":
        return "end"
    elif state.ready_for_synthesis:
        return "synthesize"
    else:
        # Need more research - create follow-up plan
        return "plan"


def should_continue_after_synthesis(_state: AgentState) -> Literal["end"]:
    """
    Routing function after synthesis.
    Always end after synthesis is complete.
    """
    return "end"


def create_research_graph():
    """
    Create the main research agent graph.

    Flow:
    1. START -> Planning Node
    2. Planning -> Execution Node
    3. Execution -> Evaluation Node
    4. Evaluation -> (Synthesis if ready) OR (Planning if more research needed)
    5. Synthesis -> END
    """

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("plan", planning_node)
    workflow.add_node("execute", execution_node)
    workflow.add_node("evaluate", evaluation_node)
    workflow.add_node("synthesize", synthesis_node)

    # Set the entry point
    workflow.set_entry_point("plan")

    # Add edges
    workflow.add_conditional_edges(
        "plan",
        should_continue_after_planning,
        {
            "execute": "execute",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "execute",
        should_continue_after_execution,
        {
            "evaluate": "evaluate",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "evaluate",
        should_continue_after_evaluation,
        {
            "synthesize": "synthesize",
            "plan": "plan",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "synthesize",
        should_continue_after_synthesis,
        {
            "end": END
        }
    )

    # Compile and return the graph
    return workflow.compile()


# Create the graph instance
research_graph = create_research_graph()
