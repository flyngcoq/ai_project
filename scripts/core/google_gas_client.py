import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env from scripts/.env
load_dotenv(Path(__file__).parent.parent / ".env")

GAS_URL = os.getenv("GAS_URL")
GAS_TOKEN = os.getenv("GAS_TOKEN")

def call_gas(action, **kwargs):
    if not GAS_URL or not GAS_TOKEN:
        return "Error: GAS configuration missing in .env"
    
    payload = {
        "token": GAS_TOKEN,
        "action": action
    }
    payload.update(kwargs)
    
    try:
        # Google Apps Script redirection requires following redirects
        response = requests.post(GAS_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

# Convenience functions
def list_calendar_events():
    return call_gas("listEvents")

def add_calendar_event(title, start_time, end_time):
    return call_gas("addEvent", title=title, startTime=start_time, endTime=end_time)

def list_unread_emails():
    return call_gas("listEmails")
