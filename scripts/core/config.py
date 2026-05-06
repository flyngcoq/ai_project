import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the scripts directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma4:26b-a4b-it-q4_K_M"

VAULT_DIR = Path("/Users/flyngcoq/AI_Project/Obsidian_Vault")
INBOX_DIR = VAULT_DIR / "00_Inbox"
FLEETING_DIR = VAULT_DIR / "10_Fleeting_Notes"
LIT_DIR = VAULT_DIR / "20_Literature_Notes"
PERM_DIR = VAULT_DIR / "30_Permanent_Notes"
ARCHIVE_DIR = VAULT_DIR / "Archive"

SEARCH_DIRS = [PERM_DIR, LIT_DIR, FLEETING_DIR]
