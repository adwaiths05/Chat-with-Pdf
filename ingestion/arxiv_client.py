import re
from ingestion.mcp.client import MCPClient
from ingestion.latex_parser import latex_to_text


_ARXIV_ID_RE = re.compile(r"^\d{4}\.\d{4,5}(v\d+)?$")  # simple new-style id check


class ArxivMCP:
    """
    High-level wrapper:
    - accepts title OR arXiv id
    - if title, searches and picks the top hit
    - fetches LaTeX from server
    - converts to plain text via latex_to_text()
    """

    def __init__(self, server_cmd=None, cwd=None):
        self.client = MCPClient(server_cmd=server_cmd, cwd=cwd)

    def _resolve_id(self, title_or_id: str) -> str:
        if _ARXIV_ID_RE.match(title_or_id.strip()):
            return title_or_id.strip()

        # Otherwise treat as a query string; pick best match
        resp = self.client.call("search_papers", {"query": title_or_id, "max_results": 1})
        if "error" in resp:
            raise RuntimeError(resp["error"]["message"])
        papers = resp["result"].get("papers", [])
        if not papers:
            raise ValueError(f"No arXiv paper found for query: {title_or_id}")
        return papers[0]["id"]

    def fetch_paper(self, title_or_id: str):
        arxiv_id = self._resolve_id(title_or_id)
        resp = self.client.call("get_latex", {"id": arxiv_id})
        if "error" in resp:
            raise RuntimeError(resp["error"]["message"])
        latex = resp["result"]["latex"]
        plain = latex_to_text(latex)
        return arxiv_id, plain

    def close(self):
        self.client.close()
