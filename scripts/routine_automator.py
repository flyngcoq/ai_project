import schedule
import time
import datetime
from pathlib import Path

# Configuration
VAULT_DIR = Path("/Users/flyngcoq/AI_Project/Obsidian_Vault")
DAILY_LOGS_DIR = VAULT_DIR / "40_Projects" / "Daily_Logs"

def ensure_dir(path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def generate_daily_note():
    ensure_dir(DAILY_LOGS_DIR)
    
    today = datetime.datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    note_path = DAILY_LOGS_DIR / f"{date_str}_Daily_Log.md"
    
    if not note_path.exists():
        content = f"""# {date_str} Daily Log

## 🎯 오늘의 목표
- [ ] 
- [ ] 

## 📝 업무 내용 (자동화 기록)
- 

## 🤖 AI 인사이트 (Ollama 자동 요약)
- 
"""
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[{datetime.datetime.now()}] Created daily note: {note_path.name}")
    else:
        print(f"[{datetime.datetime.now()}] Daily note already exists: {note_path.name}")

def job_daily_morning():
    print("Running morning routine...")
    generate_daily_note()
    # Add other morning tasks here (e.g., fetch news, summarize emails)

# Schedule setup
# 매일 아침 8시에 데일리 노트 생성 (테스트를 위해 1분마다 실행하려면 schedule.every(1).minutes.do(job_daily_morning) 사용)
schedule.every().day.at("08:00").do(job_daily_morning)

if __name__ == "__main__":
    print("Routine Automator Started. Waiting for scheduled tasks...")
    # 테스트 용도: 시작하자마자 한 번 실행
    job_daily_morning()
    
    while True:
        schedule.run_pending()
        time.sleep(60) # 1분마다 체크
