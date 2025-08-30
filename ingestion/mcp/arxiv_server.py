#!/usr/bin/env python3
import arxiv
import json
import sys

def fetch_arxiv(arxiv_id: str) -> str:
    """Fetch LaTeX source for a given ArXiv ID."""
    search = arxiv.Search(id_list=[arxiv_id])
    paper = next(search.results())
    source_path = paper.download_source(dirpath="/tmp")
    
    # Return path to the downloaded tarball (.tar.gz)
    return source_path

def handle_request(request: dict):
    """Handle incoming MCP request."""
    method = request.get("method")
    params = request.get("params", {})

    if method == "fetch_arxiv":
        arxiv_id = params.get("id")
        result = fetch_arxiv(arxiv_id)
        return {"result": result}

    return {"error": f"Unknown method {method}"}

if __name__ == "__main__":
    # Simple stdin/stdout JSON-RPC loop
    for line in sys.stdin:
        try:
            req = json.loads(line.strip())
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()
