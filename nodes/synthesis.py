"""
Synthesis node for creating the final research report.
"""

from models import AgentState
from prompts import SYNTHESIS_AGENT_SYSTEM_PROMPT
from utils import get_llm
from langchain_core.messages import SystemMessage, HumanMessage


async def synthesis_node(state: AgentState) -> AgentState:
    """
    Synthesis node that creates the final research report.
    """
    print(f"\n{'='*80}\nSYNTHESIS NODE\n{'='*80}")

    llm = get_llm(temperature=0.3)

    try:
        report = await generate_final_report(
            query=state.query,
            plan=state.plan,
            llm=llm
        )

        state.final_report = report
        state.status = "completed"
        print(f"✓ Report generated ({len(report)} characters)")

    except Exception as e:
        print(f"✗ Synthesis failed: {e}")
        state.status = "failed"
        state.errors.append(f"Synthesis failed: {str(e)}")

    return state


async def generate_final_report(query: str, plan, llm) -> str:
    """Generate the final synthesized research report."""

    # Collect all worker outputs organized by phase
    phases_info = []
    for phase in plan.phases:
        phase_outputs = []
        for task in phase.worker_tasks:
            if task.output:
                phase_outputs.append({
                    'task_name': task.name,
                    'description': task.description,
                    'output': task.output
                })

        if phase_outputs:
            phases_info.append({
                'phase_name': phase.name,
                'phase_description': phase.description,
                'tasks': phase_outputs
            })

    synthesis_prompt = f"""
# Research Query
{query}

# Research Strategy
{plan.strategy_rationale}

# Research Findings

{format_phases_for_synthesis(phases_info)}

# Your Task
Create a comprehensive, well-structured research report that:

1. **Synthesizes all findings** into a coherent narrative
2. **Addresses the original query** completely and thoroughly
3. **Provides clear insights** and actionable information
4. **Cites sources** where appropriate
5. **Organizes information** logically with clear sections

The report should be:
- Professional and well-formatted (use markdown)
- Comprehensive yet concise
- Evidence-based with proper attribution
- Structured with clear headings and sections
- Free of redundancy

Write the final research report now.
"""

    messages = [
        SystemMessage(content=SYNTHESIS_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=synthesis_prompt)
    ]

    response = await llm.ainvoke(messages)
    return response.content


def format_phases_for_synthesis(phases_info: list) -> str:
    """Format phase information for synthesis."""
    formatted = []

    for phase in phases_info:
        formatted.append(f"\n## Phase: {phase['phase_name']}\n")
        formatted.append(f"**Purpose:** {phase['phase_description']}\n")

        for task in phase['tasks']:
            formatted.append(f"\n### {task['task_name']}\n")
            formatted.append(f"*{task['description']}*\n")
            formatted.append(f"\n{task['output']}\n")

    return "\n".join(formatted)
