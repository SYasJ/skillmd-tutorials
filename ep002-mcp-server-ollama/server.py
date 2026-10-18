import json
import urllib.request

from mcp.server import MCPServer

mcp = MCPServer("repo-stats")


@mcp.tool()
def repo_stats(repo: str) -> dict:
    """Live GitHub stats for a repo, e.g. 'ollama/ollama'."""
    url = f"https://api.github.com/repos/{repo}"
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.load(r)
    return {
        "repo": d["full_name"],
        "stars": d["stargazers_count"],
        "forks": d["forks_count"],
        "license": (d.get("license") or {}).get("spdx_id"),
    }


if __name__ == "__main__":
    mcp.run()  # stdio by default
