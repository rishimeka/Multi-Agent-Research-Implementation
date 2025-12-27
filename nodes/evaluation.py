"""
Evaluation node for assessing research completeness and identifying gaps.
"""

from typing import List
from models import AgentState, EvaluationResult, ExecutionPlan
from prompts import EVALUATION_AGENT_SYSTEM_PROMPT
from utils import get_llm
from langchain_core.messages import SystemMessage, HumanMessage


async def evaluation_node(state: AgentState) -> AgentState:
    """
    Evaluation node that assesses research completeness and identifies gaps.
    """
    print(f"\n{'='*80}\nEVALUATION NODE\n{'='*80}")

    # Check if we've already done multiple iterations
    MAX_PLANNING_ITERATIONS = 3
    if state.planning_iteration >= MAX_PLANNING_ITERATIONS:
        print(f"⚠ Maximum planning iterations ({MAX_PLANNING_ITERATIONS}) reached.")
        print("→ Proceeding to synthesis with current information")
        state.ready_for_synthesis = True
        state.status = "synthesizing"
        return state

    llm = get_llm(temperature=0)

    try:
        evaluation = await evaluate_research_completeness(
            query=state.query,
            plan=state.plan,
            llm=llm,
            iteration=state.planning_iteration
        )

        # Store the evaluation result
        state.evaluation = evaluation

        print(f"✓ Completeness score: {evaluation.completeness_score:.2f}")
        print(f"✓ Research complete: {evaluation.is_complete}")

        if evaluation.is_complete:
            print("→ Proceeding to synthesis")
            state.ready_for_synthesis = True
            state.status = "synthesizing"
        else:
            print(f"→ Identified {len(evaluation.missing_aspects)} gaps - will create follow-up plan")
            # Need more research - will trigger re-planning
            state.plan.needs_additional_research = True
            state.status = "planning"  # Will create follow-up plan

            # Store gaps for follow-up planning
            state.identified_gaps.extend(evaluation.missing_aspects)

    except Exception as e:
        print(f"✗ Evaluation failed: {e}")
        state.status = "failed"
        state.errors.append(f"Evaluation failed: {str(e)}")

    return state


async def evaluate_research_completeness(
    query: str,
    plan: ExecutionPlan,
    llm,
    iteration: int = 0
) -> EvaluationResult:
    """Evaluate if the research plan has sufficient information."""

    structured_llm = llm.with_structured_output(EvaluationResult)

    # Collect all worker outputs
    all_outputs = []
    for phase in plan.phases:
        for task in phase.worker_tasks:
            if task.output:
                all_outputs.append({
                    'phase': phase.name,
                    'task': task.name,
                    'output': task.output
                })

    iteration_context = ""
    if iteration > 0:
        iteration_context = f"\n**Note**: This is planning iteration {iteration + 1}. We have limited iterations remaining, so be more accepting of good-enough results."

    evaluation_prompt = f"""
Evaluate the completeness of this research:

## Original Query
{query}

## Research Strategy Used
{plan.strategy_rationale}

## Gathered Information

{format_outputs(all_outputs)}
{iteration_context}

## Your Task
Assess whether this information is sufficient to create a comprehensive report that fully addresses the query.

**Remember:**
- Score ≥ 0.7 → Mark as complete (is_complete=true)
- Score 0.5-0.7 → Mark as complete unless gaps are truly critical
- If 70%+ of query is well-addressed → Mark as complete
- Consider: Can we write a good report with this? (Not: Is this perfect?)

Consider:
1. Coverage: Are all aspects of the query addressed?
2. Depth: Is there enough detail and context?
3. Quality: Are sources authoritative and recent?
4. Coherence: Can this be synthesized into a coherent report?

Provide your evaluation with specific missing_aspects if incomplete, or confirm readiness if complete.
"""

    messages = [
        SystemMessage(content=EVALUATION_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=evaluation_prompt)
    ]

    evaluation = await structured_llm.ainvoke(messages)
    return evaluation


def format_outputs(outputs: List[dict]) -> str:
    """Format worker outputs for evaluation."""
    formatted = []
    for i, output in enumerate(outputs, 1):
        formatted.append(f"""
### Finding {i}: {output['task']} (Phase: {output['phase']})
{output['output'][:500]}{'...' if len(output['output']) > 500 else ''}
""")
    return "\n".join(formatted)