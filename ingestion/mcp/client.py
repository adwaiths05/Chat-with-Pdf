import subprocess
import json

class MCPClient:
    def __init__(self, server_cmd=["python", "ingestion/mcp/arxiv_server.py"]):
        self.process = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

    def call(self, method: str, params: dict) -> dict:
        """Send a request and wait for response."""
        request = {"method": method, "params": params}
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        response = self.process.stdout.readline()
        return json.loads(response)

    def close(self):
        self.process.terminate()
