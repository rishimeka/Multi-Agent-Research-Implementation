"""
Execution node for carrying out tasks based on the execution plan.
"""

import asyncio
import random
from models import AgentState
from nodes.worker_agent import create_worker_graph, WorkerAgentState

# Maximum number of workers executing concurrently
CONCURRENT_WORKER_LIMIT = 3


async def execution_node(state: AgentState) -> AgentState:
    """
    Execution node that carries out the tasks defined in the execution plan.
    Executes phases sequentially, but workers within each phase run in parallel.
    """
    print(f"\n{'='*80}\nEXECUTION NODE\n{'='*80}\nTotal phases to execute: {len(state.plan.phases)}\n")

    try:
        # Execute each phase sequentially
        for phase_idx, phase in enumerate(state.plan.phases, 1):
            print(f"\nExecuting Phase {phase_idx}/{len(state.plan.phases)}: {phase.name}")
            phase.status = "in_progress"
            
            # Execute all worker tasks in this phase in PARALLEL
            await execute_phase_parallel(phase)
            
            # Check if any tasks failed
            failed_tasks = [t for t in phase.worker_tasks if t.status == "failed"]
            
            if failed_tasks:
                phase.status = "failed"
                phase.error = f"{len(failed_tasks)} of {len(phase.worker_tasks)} task(s) failed"
                for task in failed_tasks:
                    state.errors.append(f"Task '{task.name}' ({task.task_id}) failed: {task.error}")
            else:
                phase.status = "completed"
                print(f"  ✓ Phase {phase_idx} completed successfully")

        # After all phases complete, move to evaluation
        state.status = "evaluating"
        
    except Exception as e:
        state.status = "failed"
        state.errors.append(f"Execution failed: {str(e)}")

    return state


async def execute_phase_parallel(phase):
    """Execute all worker tasks in a phase with controlled concurrency."""

    tasks = phase.worker_tasks

    # Create semaphore to limit concurrent workers
    semaphore = asyncio.Semaphore(CONCURRENT_WORKER_LIMIT)

    async def execute_with_limit(task):
        """Execute a single worker with rate limiting."""
        async with semaphore:
            # Add small random delay to spread out requests
            await asyncio.sleep(random.uniform(0.1, 0.5))

            task.status = "in_progress"

            # Create worker graph for this task
            worker_graph = create_worker_graph(task)

            # Create initial state for worker (as dict, not Pydantic model)
            worker_state = {
                "task": task,
                "messages": [],
                "final_result": "",
                "llm": None,
                "iteration_count": 0,
                "tool_calls_count": 0
            }

            # Execute with recursion limit config
            return await worker_graph.ainvoke(
                worker_state,
                config={"recursion_limit": 50}
            )

    # Execute all workers with controlled concurrency
    print(f"  Executing {len(tasks)} workers (max {CONCURRENT_WORKER_LIMIT} concurrent)...")
    worker_coros = [execute_with_limit(task) for task in tasks]
    results = await asyncio.gather(*worker_coros, return_exceptions=True)

    # Process results and update tasks
    for task, result in zip(tasks, results):
        if isinstance(result, Exception):
            task.status = "failed"
            task.error = str(result)
            print(f"    ✗ Worker '{task.name}' failed: {result}")
        else:
            # Extract final result and tool call count from worker state
            task.output = result.get("final_result", "")
            task.tool_calls_made = result.get("tool_calls_count", 0)
            task.status = "completed"
            print(f"    ✓ Worker '{task.name}' completed ({task.tool_calls_made} tool calls)")