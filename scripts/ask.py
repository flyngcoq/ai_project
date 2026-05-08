import sys
from pathlib import Path

# Add project root and agents directory to path
root = Path(__file__).parent.parent
sys.path.append(str(root))
sys.path.append(str(root / "scripts" / "agents")) # For telegram_bot

from core.orchestrator import orchestrate_agents
try:
    from agents.telegram_bot import retrieve_context
except ImportError:
    from telegram_bot import retrieve_context

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/ask.py \"your question\"")
        return

    query = " ".join(sys.argv[1:])
    print(f"🤔 오케스트레이터 가동 중: \"{query}\"")
    
    # Get context (shared logic from telegram_bot)
    context_data = retrieve_context(query)
    
    # Orchestrate
    response = orchestrate_agents(query, context_data)
    
    print("\n" + "="*50)
    print(response)
    print("="*50)

if __name__ == "__main__":
    main()
