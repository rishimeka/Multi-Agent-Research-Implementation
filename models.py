from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class WorkerTask(BaseModel):
    """A task executed by a worker agent that runs in parallel with other workers in the same phase."""

    task_id: str = Field(
        description="Unique identifier for this worker task"
    )

    name: str = Field(
        description="Human-readable name for this worker task"
    )

    description: str = Field(
        description="What this worker task accomplishes"
    )

    detailed_task_outline: str = Field(
        description="""
        Comprehensive task outline including:
        1. What to do
        2. How to do it  
        3. What constitutes success
        4. Output format
        """
    )

    needs_web_search: bool = Field(
        default=False,
        description="Whether this worker requires web search functionality"
    )

    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="LLM temperature for this task (0.0=deterministic, 1.0=creative). Use lower for factual research, higher for synthesis/analysis"
    )

    expected_output: str = Field(
        description="Expected format and content of the output"
    )

    output: Optional[str] = Field(
        default=None,
        description="Results produced by the worker agent"
    )

    status: str = Field(
        default="pending",
        description="Execution state: 'pending', 'in_progress', 'completed', or 'failed'"
    )

    error: Optional[str] = Field(
        default=None,
        description="Error message if task failed"
    )

    tool_calls_made: int = Field(
        default=0,
        description="Number of tool calls made by this worker"
    )


class ExecutionPhase(BaseModel):
    """A sequential phase containing parallel worker tasks."""

    phase_id: str = Field(
        description="Unique identifier for this execution phase"
    )

    name: str = Field(
        description="Human-readable name for this phase"
    )

    description: str = Field(
        description="What this phase accomplishes in the overall plan"
    )

    worker_tasks: List[WorkerTask] = Field(
        default_factory=list,
        description="Worker tasks executed concurrently within this phase"
    )

    status: str = Field(
        default="pending",
        description="Execution state: 'pending', 'in_progress', 'completed', or 'failed'"
    )

    error: Optional[str] = Field(
        default=None,
        description="Error message if phase failed"
    )


class ExecutionPlan(BaseModel):
    """Multi-agent execution plan with sequential phases of parallel worker tasks."""

    summary: str = Field(
        description="Overview of the plan's objectives"
    )

    phases: List[ExecutionPhase] = Field(
        description="Sequentially ordered execution phases"
    )

    strategy_rationale: str = Field(
        description="Strategic approach and reasoning for this plan structure"
    )

    needs_additional_research: bool = Field(
        default=True,
        description="Whether additional research iterations are needed after plan completion"
    )


class EvaluationResult(BaseModel):
    """Results from the evaluation phase."""

    is_complete: bool = Field(
        description="Whether the research objective has been fully met"
    )

    completeness_score: float = Field(
        ge=0.0,
        le=1.0,
        description="0-1 score indicating how complete the research is"
    )

    missing_aspects: List[str] = Field(
        description="List of missing aspects that need to be researched"
    )

    recommendation: str = Field(
        description="Next step recommendation: 'continue', 'conclude', or 'escalate'"
    )

    justification: str = Field(
        description="Detailed reasoning for the evaluation and recommendation"
    )


class AgentState(BaseModel):
    """
    Comprehensive state of the research agent within the multi-agent research graph.
    """

    # ==================== INPUT ====================
    query: str = Field(
        description="The user's research query"
    )

    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context passed between graph nodes"
    )

    # ==================== PLANNING ====================
    plan: Optional[ExecutionPlan] = Field(
        default=None,
        description="Current active ExecutionPlan being executed"
    )

    plan_history: List[ExecutionPlan] = Field(
        default_factory=list,
        description="History of all ExecutionPlans generated (for iteration tracking)"
    )

    planning_iteration: int = Field(
        default=0,
        description="Number of planning iterations performed"
    )

    # ==================== EXECUTION ====================
    current_phase_index: int = Field(
        default=0,
        description="Index of currently executing phase in plan.phases"
    )
    
    # ==================== EVALUATION ====================
    evaluation: Optional[EvaluationResult] = Field(
        default=None,
        description="Result of evaluating research completeness after execution"
    )

    identified_gaps: List[str] = Field(
        default_factory=list,
        description="Accumulated research gaps identified across evaluation iterations"
    )

    # ==================== SYNTHESIS ====================
    ready_for_synthesis: bool = Field(
        default=False,
        description="Flag indicating all phases complete and ready for final synthesis"
    )

    final_report: Optional[str] = Field(
        default=None,
        description="Final synthesized research report"
    )

    # ==================== STATUS TRACKING ====================
    status: str = Field(
        default="planning",
        description="Graph state: 'planning', 'executing', 'evaluating', 'synthesizing', 'completed', or 'failed'"
    )

    errors: List[str] = Field(
        default_factory=list,
        description="Accumulated errors from any node"
    )
    
    # ==================== COST & EFFICIENCY TRACKING ====================
    total_tool_calls: int = Field(
        default=0,
        description="Total tool calls across all workers"
    )
    
    total_tokens_used: int = Field(
        default=0,
        description="Total tokens used (if tracking)"
    )