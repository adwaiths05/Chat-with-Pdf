import subprocess
import json
import threading
import queue
import os
from typing import Any, Dict, Optional


class MCPClient:
    """
    Lightweight client that spawns the Python MCP server and speaks
    newline-delimited JSON over stdin/stdout.
    """
    def __init__(self, server_cmd=None, cwd: Optional[str] = None):
        if server_cmd is None:
            # Default to your server in this repo
            server_cmd = ["python", "ingestion/mcp/arxiv_server.py"]

        self.proc = subprocess.Popen(
            server_cmd,
            cwd=cwd or None,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # line-buffered
        )

        self._out_q = queue.Queue()
        self._reader_t = threading.Thread(target=self._read_stdout, daemon=True)
        self._reader_t.start()

        self._req_id = 0

    def _read_stdout(self):
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            self._out_q.put(line.rstrip("\n"))

    def call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if self.proc.poll() is not None:
            raise RuntimeError("MCP server process is not running")

        self._req_id += 1
        req = {"id": self._req_id, "method": method, "params": params or {}}
        payload = json.dumps(req)

        assert self.proc.stdin is not None
        self.proc.stdin.write(payload + "\n")
        self.proc.stdin.flush()

        # Wait for matching id
        while True:
            line = self._out_q.get()  # blocking
            try:
                resp = json.loads(line)
            except json.JSONDecodeError:
                continue
            if resp.get("id") == self._req_id:
                return resp

    def close(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
