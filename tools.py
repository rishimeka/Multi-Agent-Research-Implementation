from langchain.tools import tool
from helpers import _search, _fetch, _search_and_fetch


@tool
def search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web and return a list of results with title, url, and snippet.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        List of dicts with 'title', 'url', and 'snippet' fields
    """
    results = _search(query, max_results)
    return [r.model_dump() for r in results]


@tool
def fetch(url: str) -> dict:
    """Fetch a webpage and return its main content as markdown.
    
    Args:
        url: The URL to fetch
    
    Returns:
        Dict with 'url' and 'content' (markdown) fields
    """
    result = _fetch(url)
    return result.model_dump()


@tool
def search_and_fetch(query: str, max_results: int = 3) -> list[dict]:
    """Search and fetch content from top results in one step.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to fetch (default: 3)
    
    Returns:
        List of dicts with 'title', 'url', 'snippet', and 'content' fields
    """
    results = _search_and_fetch(query, max_results)
    return [r.model_dump() for r in results]


def get_all_tools() -> list:
    """Return a list of all available tools."""
    return [search, fetch, search_and_fetch]