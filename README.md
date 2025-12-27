# Multi-Agent Research System

A production-grade autonomous research system built with LangGraph that orchestrates multiple AI agents to conduct comprehensive research on any topic.

## Architecture

This system implements a **hybrid multi-agent architecture** with:
- **Sequential phase execution** for logical research progression
- **Parallel worker agents** within each phase for speed
- **Iterative refinement** through evaluation loops
- **Self-correcting capabilities** via gap analysis and replanning

### System Flow

```
  ┌─────────────┐
  │    START    │
  └──────┬──────┘
         │
         ▼
┌─────────────────┐
│    PLANNING     │  Creates structured execution plan
│     AGENT       │  with sequential phases & parallel tasks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  EXECUTION      │  Executes phases sequentially
│  ENGINE         │  Workers run in parallel per phase
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  EVALUATION     │  Assesses research completeness
│  AGENT          │  Identifies gaps if needed
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐  ┌──────────┐
│ Gaps?  │  │ Complete │
│ Re-plan│  │ Synthesis│
└───┬────┘  └────┬─────┘
    │            │
    └───────┬────┘
            ▼
       ┌──────────┐
       │   END    │
       └──────────┘
```

## Core Components

### 1. Planning Agent ([nodes/planning.py](nodes/planning.py))
- Analyzes research queries
- Creates structured execution plans
- Handles follow-up planning for identified gaps
- Uses structured output (Pydantic models)

### 2. Execution Engine ([nodes/execution.py](nodes/execution.py))
- Executes phases sequentially
- Runs worker agents in parallel using `asyncio.gather()`
- Handles errors gracefully
- Tracks execution state

### 3. Worker Agents ([nodes/worker_agent.py](nodes/worker_agent.py))
- Individual research tasks
- Tool-enabled (web search, fetch, search+fetch)
- Sub-graphs with tool calling loops
- Configurable temperature and tools

### 4. Evaluation Agent ([nodes/evaluation.py](nodes/evaluation.py))
- Assesses research completeness
- Identifies specific gaps
- Provides completeness scoring
- Triggers iteration if needed

### 5. Synthesis Agent ([nodes/synthesis.py](nodes/synthesis.py))
- Aggregates all findings
- Creates comprehensive reports
- Professional markdown formatting
- Source attribution

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd multi-agent-research

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Requirements

Create a `requirements.txt` with:

```txt
langchain>=0.1.0
langchain-openai>=0.0.5
langgraph>=0.0.20
pydantic>=2.0.0
python-dotenv>=1.0.0
```

## Configuration

Create a `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Basic Usage

```python
import asyncio
from models import AgentState
from nodes.research_agent import research_graph

async def research(query: str):
    initial_state = AgentState(query=query)
    result = await research_graph.ainvoke(initial_state)
    return result.final_report

# Run research
report = asyncio.run(research("What are the latest developments in AI safety?"))
print(report)
```

### Using main.py

```bash
python main.py
```

This runs a comprehensive AI safety research query and saves the output to `reports/ai_safety_research_report.md`.

### Running Tests

```bash
python test.py
```

Runs three test scenarios:
1. **Simple Research**: Basic single-topic query
2. **Complex Research**: Multi-part comprehensive query
3. **Iterative Research**: Tests the iteration mechanism

## Data Models

### AgentState

The central state object that flows through the graph:

```python
class AgentState(BaseModel):
    # Input
    query: str

    # Planning
    plan: Optional[ExecutionPlan]
    plan_history: List[ExecutionPlan]
    planning_iteration: int

    # Execution
    current_phase_index: int

    # Evaluation
    evaluation: Optional[EvaluationResult]
    identified_gaps: List[str]

    # Synthesis
    ready_for_synthesis: bool
    final_report: Optional[str]

    # Status
    status: str  # "planning", "executing", "evaluating", "synthesizing", "completed", "failed"
    errors: List[str]
```

### ExecutionPlan

Structured plan with phases and worker tasks:

```python
class ExecutionPlan(BaseModel):
    summary: str
    phases: List[ExecutionPhase]  # Sequential
    strategy_rationale: str
    needs_additional_research: bool

class ExecutionPhase(BaseModel):
    phase_id: str
    name: str
    description: str
    worker_tasks: List[WorkerTask]  # Parallel within phase
```

### WorkerTask

Individual research task specification:

```python
class WorkerTask(BaseModel):
    task_id: str
    name: str
    description: str
    detailed_task_outline: str
    needs_web_search: bool
    temperature: float
    expected_output: str
    output: Optional[str]
    status: str
```

## Key Features

### ✅ Parallel Execution
- Workers within a phase run concurrently using `asyncio`
- Phases execute sequentially for logical progression
- Maximum throughput without sacrificing coherence

### ✅ Iterative Refinement
- Evaluation agent identifies gaps
- System automatically creates follow-up plans
- Continues until research is comprehensive

### ✅ Tool Integration
- Web search for current information
- URL fetching for detailed content
- Combined search+fetch for efficiency

### ✅ Error Handling
- Graceful degradation on worker failures
- Detailed error tracking and reporting
- Phase-level and task-level error isolation

### ✅ Structured Outputs
- All agent outputs use Pydantic models
- Type-safe state management
- Easy to extend and modify

### ✅ Professional Reports
- Markdown-formatted output
- Source citations
- Metadata and timestamps
- Ready for publication

## Customization

### Adding New Tools

Edit `tools.py`:

```python
@tool
def your_custom_tool(param: str) -> dict:
    """Your tool description."""
    # Implementation
    return result

def get_all_tools():
    return [search, fetch, search_and_fetch, your_custom_tool]
```

### Modifying Prompts

Edit files in `prompts/`:
- `planning_agent.md` - Planning strategy
- `worker_agent_prompt.md` - Worker behavior
- `evaluation_agent.md` - Evaluation criteria
- `synthesis_agent.md` - Report formatting

### Changing LLM

Edit `utils.py`:

```python
def get_llm(temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4",  # Change model here
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
```

## Performance

**Typical Research Query:**
- Planning: ~5-10 seconds
- Execution: 30-120 seconds (depending on parallel workers)
- Evaluation: ~5 seconds
- Synthesis: ~10-15 seconds

**Total**: 50-150 seconds for comprehensive research

**Factors:**
- Number of phases: More phases = longer execution
- Workers per phase: Parallelized, minimal impact
- Tool usage: Web searches add latency
- Iteration: Additional loops multiply time

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "API key not found"
Check your `.env` file contains `OPENAI_API_KEY=...`

### Workers failing
- Check API rate limits
- Verify internet connection for web tools
- Review error messages in `state.errors`

### No iteration happening
- Evaluation agent may be too lenient
- Adjust completeness threshold in evaluation prompt
- Check `state.identified_gaps` for gap detection

## Architecture Decisions

### Why LangGraph?
- Native support for cyclic graphs (evaluation → planning loop)
- Type-safe state management
- Excellent debugging and visualization tools

### Why Hybrid Execution?
- Sequential phases ensure logical research flow
- Parallel workers maximize throughput
- Best of both worlds: speed + coherence

### Why Pydantic Models?
- Structured LLM outputs (no parsing needed)
- Type safety throughout the system
- Easy validation and serialization

### Why Separate Worker Graphs?
- Isolation: Each worker is independent
- Tool calling loops: Workers can iteratively use tools
- Reusability: Same worker logic for all tasks

## Future Enhancements

- [ ] Add support for document upload and analysis
- [ ] Implement memory/RAG for long-term context
- [ ] Add streaming output for real-time progress
- [ ] Support multiple LLM providers (Anthropic, Gemini, etc.)
- [ ] Add visualization of execution graph
- [ ] Implement cost tracking and optimization
- [ ] Add human-in-the-loop approval for plans

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Credits

Built with:
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [OpenAI](https://openai.com/)
- [Anthropic "How we built our multi-agent research system"](https://www.anthropic.com/engineering/multi-agent-research-system)
