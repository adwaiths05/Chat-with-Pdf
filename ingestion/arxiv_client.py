from ingestion.mcp.client import MCPClient
from ingestion.latex_parser import latex_to_text

class ArxivMCP:
    def __init__(self):
        self.client = MCPClient(config_path="ingestion/mcp/arxiv_server.json")

    def fetch_paper(self, paper_title: str):
        #  Search for the paper
        search_result = self.client.call("search_papers", {"title": paper_title})
        if not search_result.get("result") or not search_result["result"].get("papers"):
            raise ValueError(f"No papers found for '{paper_title}'")
        paper = search_result["result"]["papers"][0]
        paper_id = paper["id"]

        #  Fetch LaTeX content
        latex_content_resp = self.client.call("get_paper_content", {"id": paper_id})
        if "result" not in latex_content_resp or "content" not in latex_content_resp["result"]:
            raise RuntimeError(f"Failed to get content for paper {paper_id}")
        latex_content = latex_content_resp["result"]["content"]

        #  Convert to plain text
        clean_text = latex_to_text(latex_content)
        return paper_id, clean_text
from ingestion.mcp.client import MCPClient

class ArxivClient:
    def __init__(self):
        self.client = MCPClient()

    def fetch(self, arxiv_id: str) -> str:
        """Fetch LaTeX source for a paper via MCP server."""
        response = self.client.call("fetch_arxiv", {"id": arxiv_id})
        if "error" in response:
            raise RuntimeError(response["error"])
        return response["result"]

    def close(self):
        self.client.close()
