"""
Planning node for generating execution plans based on user queries.
"""

from models import AgentState, ExecutionPlan
from prompts import PLANNING_AGENT_SYSTEM_PROMPT
from utils import get_llm
from langchain_core.messages import SystemMessage, HumanMessage


async def planning_node(state: AgentState) -> AgentState:
    """
    Planning node that generates an execution plan based on the user's query.
    """
    iteration = state.planning_iteration + 1
    print(f"\n{'='*80}\nPLANNING NODE - Iteration {iteration}\n{'='*80}")

    # Check if we've exceeded maximum planning iterations
    total_phases = sum(len(p.phases) for p in state.plan_history)
    if total_phases >= 10:
        print(f"⚠ Maximum phase limit reached ({total_phases} phases). Skipping additional planning.")
        state.status = "synthesizing"
        state.ready_for_synthesis = True
        return state

    llm = get_llm(temperature=0)

    try:
        # Pass gaps if this is a follow-up iteration
        gaps = state.identified_gaps if state.planning_iteration > 0 else None

        if gaps:
            print(f"Follow-up planning to address {len(gaps)} identified gaps")
            print(f"Total phases so far: {total_phases}/10")
        else:
            print("Initial planning phase")

        plan = await generate_execution_plan(state.query, llm, gaps, total_phases)

        # Enforce constraints on the generated plan
        plan = enforce_plan_constraints(plan)

        print(f"✓ Created plan with {len(plan.phases)} phases")
        total_tasks = sum(len(phase.worker_tasks) for phase in plan.phases)
        print(f"✓ Total worker tasks: {total_tasks}")

        state.plan = plan
        state.plan_history.append(plan)
        state.planning_iteration += 1
        state.status = "executing"
    except Exception as e:
        print(f"✗ Planning failed: {e}")
        state.status = "failed"
        state.errors.append(f"Planning failed: {str(e)}")

    return state


async def generate_execution_plan(query: str, llm, gaps: list = None, total_phases: int = 0) -> ExecutionPlan:
    """
    Generate an execution plan using structured output.

    Args:
        query: The original research query
        llm: The language model to use
        gaps: Optional list of identified research gaps for follow-up planning
        total_phases: Number of phases already executed across all iterations
    """
    structured_llm = llm.with_structured_output(ExecutionPlan)

    # Calculate remaining phase budget
    remaining_phases = max(1, 10 - total_phases)

    if gaps:
        # Follow-up planning with gaps
        gaps_text = "\n".join(f"- {gap}" for gap in gaps)
        prompt = f"""Create a follow-up execution plan to address these research gaps:

Original Query: {query}

Identified Gaps:
{gaps_text}

IMPORTANT CONSTRAINTS:
- You have {remaining_phases} phases remaining (total limit is 10 phases)
- Maximum 4 workers per phase
- Each worker should complete in 5-10 tool calls

Create a focused, efficient plan to fill these specific gaps with targeted research tasks."""
    else:
        # Initial planning
        prompt = f"""Create an execution plan for the following research query:

{query}

IMPORTANT CONSTRAINTS:
- Maximum 4 workers per phase
- Design for 2-4 phases (maximum 10 total across all iterations)
- Each worker should complete in 5-10 tool calls"""

    messages = [
        SystemMessage(content=PLANNING_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]

    plan = await structured_llm.ainvoke(messages)
    return plan


def enforce_plan_constraints(plan: ExecutionPlan) -> ExecutionPlan:
    """
    Enforce hard constraints on the generated plan.
    Truncates phases and workers if they exceed limits.
    """
    # Limit to maximum 4 phases (will be checked against total later)
    if len(plan.phases) > 4:
        print(f"  ⚠ Plan had {len(plan.phases)} phases, truncating to 4")
        plan.phases = plan.phases[:4]

    # Limit workers per phase to 4
    for phase in plan.phases:
        if len(phase.worker_tasks) > 4:
            print(f"  ⚠ Phase '{phase.name}' had {len(phase.worker_tasks)} workers, truncating to 4")
            phase.worker_tasks = phase.worker_tasks[:4]

    return plan