#!/usr/bin/env python3
"""
Minimal MCP-like server over stdin/stdout.

Methods:
- search_papers { "query": "<title or keywords>", "max_results": 5 }
- get_latex     { "id": "YYMM.NNNNN" }  -> concatenated .tex text

Reply shape:
{ "id": <same as request>, "result": <payload> } or { "id": ..., "error": {"message": "..."} }
"""

import sys
import json
import tempfile
import tarfile
import os
import arxiv


def search_papers(query: str, max_results: int = 5):
    results = []
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    for r in search.results():
        results.append({
            "id": r.get_short_id(),          # e.g., "2301.12345"
            "title": r.title,
            "authors": [a.name for a in r.authors],
            "primary_category": r.primary_category,
            "updated": r.updated.isoformat() if r.updated else None,
        })
    return {"papers": results}


def get_latex(arxiv_id: str):
    # Download source tarball to temp dir and extract all .tex files
    it = arxiv.Search(id_list=[arxiv_id]).results()
    r = next(it, None)
    if r is None:
        raise ValueError(f"No result for arXiv id: {arxiv_id}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = r.download_source(dirpath=tmpdir)  # .tar.gz path
        if not os.path.exists(tar_path):
            raise RuntimeError(f"Failed to download source for {arxiv_id}")

        combined_latex = []
        with tarfile.open(tar_path, "r:gz") as tar:
            safe_members = [m for m in tar.getmembers() if m.isfile()]
            for m in safe_members:
                if m.name.lower().endswith(".tex"):
                    f = tar.extractfile(m)
                    if f is not None:
                        try:
                            combined_latex.append(f.read().decode("utf-8", errors="ignore"))
                        finally:
                            f.close()

    return {
        "id": arxiv_id,
        "latex": "\n\n".join(combined_latex).strip()
    }


def handle(request: dict):
    method = request.get("method")
    params = request.get("params", {}) or {}
    req_id = request.get("id")

    try:
        if method == "search_papers":
            query = params.get("query", "")
            max_results = int(params.get("max_results", 5))
            result = search_papers(query, max_results)
        elif method == "get_latex":
            arxiv_id = params.get("id")
            if not arxiv_id:
                raise ValueError("Missing 'id' in params")
            result = get_latex(arxiv_id)
        else:
            raise ValueError(f"Unknown method '{method}'")

        return {"id": req_id, "result": result}
    except Exception as e:
        return {"id": req_id, "error": {"message": str(e)}}


def main():
    # newline-delimited JSON requests
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            sys.stdout.write(json.dumps({"id": None, "error": {"message": f"bad json: {e}"}}) + "\n")
            sys.stdout.flush()
            continue

        resp = handle(req)
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
