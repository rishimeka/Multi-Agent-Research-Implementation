import os

def load_system_prompt(file_name: str) -> str:
    """Load a system prompt from the prompts directory."""
    system_prompt_path = os.path.join(
        os.path.dirname(__file__),
        file_name
    )
    with open(system_prompt_path, 'r', encoding='utf-8') as file:
        return file.read()
    
PLANNING_AGENT_SYSTEM_PROMPT = load_system_prompt('planning_agent.md')
WORKER_AGENT_SYSTEM_PROMPT = load_system_prompt('worker_agent_prompt.md')
EVALUATION_AGENT_SYSTEM_PROMPT = load_system_prompt('evaluation_agent.md')
SYNTHESIS_AGENT_SYSTEM_PROMPT = load_system_prompt('synthesis_agent.md')