import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify
from ddgs import DDGS
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """One search result from a web search."""

    title: str = Field(..., description="The title of the search result page")
    url: str = Field(..., description="The URL of the search result")
    snippet: str | None = Field(None, description="A short snippet or description of the result")
    content: str | None = Field(None, description="Full fetched markdown content (populated when fetched)")


class FetchResult(BaseModel):
    """Result of fetching a URL's content."""

    url: str = Field(..., description="The URL that was fetched")
    content: str = Field(..., description="The extracted main content in markdown format")


def _search(query: str, max_results: int = 5) -> list[SearchResult]:
    """Search the web and return a list of SearchResult models."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return [
            SearchResult(
                title=r.get("title", ""),
                url=r.get("href", ""),
                snippet=r.get("body", ""),
            )
            for r in results
        ]


def _fetch(url: str) -> FetchResult:
    """Fetch a webpage and return its main content as a FetchResult model."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = httpx.get(url, headers=headers, follow_redirects=True, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "iframe"]):
        tag.decompose()

    main_content = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", {"class": "content"})
        or soup.find("body")
    )

    if main_content:
        md = markdownify(str(main_content), heading_style="ATX", strip=["a"])
        lines = [line.strip() for line in md.splitlines() if line.strip()]
        return FetchResult(url=url, content="\n\n".join(lines))

    return FetchResult(url=url, content="")


def _search_and_fetch(query: str, max_results: int = 3) -> list[SearchResult]:
    """Search and fetch content from top results."""
    results = _search(query, max_results)
    for result in results:
        try:
            fetched = _fetch(result.url)
            result.content = fetched.content
        except Exception as e:
            result.content = f"Failed to fetch: {e}"
    return results