import subprocess
import json

class MCPClient:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)

        self.proc = subprocess.Popen(
            [self.config["command"], *self.config["args"]],
            cwd=self.config.get("cwd"),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

    def call(self, method: str, params: dict):
        """Send JSON-RPC request to MCP server and return response"""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        self.proc.stdin.write(json.dumps(request) + "\n")
        self.proc.stdin.flush()
        response_line = self.proc.stdout.readline()
        try:
            return json.loads(response_line)
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid MCP response: {response_line}")
