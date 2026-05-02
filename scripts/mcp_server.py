from typing import Any
import asyncio
# Note: Requires `mcp` package (pip install mcp)
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Please install mcp using: pip install mcp")
    exit(1)

# Initialize FastMCP Server
mcp = FastMCP("Obsidian-Local-Tools")

@mcp.tool()
def search_vault(query: str) -> str:
    """
    Search the Obsidian Vault for a specific keyword.
    
    Args:
        query: The keyword to search for.
    """
    import subprocess
    from pathlib import Path
    
    vault_path = Path("/Users/flyngcoq/AI_Project/Obsidian_Vault")
    
    try:
        # Simple ripgrep or grep command (Requires ripgrep installed for speed, or fallback to grep)
        result = subprocess.run(
            ['grep', '-rni', query, str(vault_path)], 
            capture_output=True, text=True, check=True
        )
        return f"Search results for '{query}':\n{result.stdout[:2000]}" # Limit output
    except subprocess.CalledProcessError:
        return f"No results found for '{query}' in the vault."
    except Exception as e:
        return f"Error during search: {e}"

@mcp.tool()
def append_to_inbox(title: str, content: str) -> str:
    """
    Create a new note or append content to an existing note in the Inbox.
    
    Args:
        title: The title of the note (without .md).
        content: The content to write into the note.
    """
    from pathlib import Path
    import datetime
    
    inbox_path = Path("/Users/flyngcoq/AI_Project/Obsidian_Vault/00_Inbox")
    if not inbox_path.exists():
        inbox_path.mkdir(parents=True, exist_ok=True)
        
    file_path = inbox_path / f"{title}.md"
    mode = 'a' if file_path.exists() else 'w'
    
    with open(file_path, mode, encoding='utf-8') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n\n## Added on {timestamp}\n{content}")
        
    return f"Successfully saved to {title}.md in Inbox."

if __name__ == "__main__":
    print("Starting MCP Server (Obsidian-Local-Tools)...")
    # This runs a stdio server by default. For HTTP/SSE, you'd configure it differently.
    mcp.run()
