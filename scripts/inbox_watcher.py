import time
import subprocess
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("watchdog 라이브러리가 필요합니다. 터미널에서 'pip install watchdog'을 실행해주세요.")
    exit(1)

INBOX_DIR = "/Users/flyngcoq/AI_Project/00_Inbox"

class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        allowed_extensions = {'.md', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf', '.csv', '.xlsx', '.xls'}
        if not event.is_directory and Path(event.src_path).suffix.lower() in allowed_extensions:
            print(f"\n🚀 [새 파일 감지됨] {Path(event.src_path).name}")
            print("AI 자동 요약 파이프라인을 가동합니다...")
            
            try:
                import sys
                import shutil
                
                # Only check for triggers in markdown files
                content = ""
                if event.src_path.endswith('.md'):
                    with open(event.src_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                if "@confl 주간보고 작성" in content:
                    print("🔔 Confluence 주간 보고서 트리거 감지! (generate_report.py 실행)")
                    report_script_path = Path(__file__).parent / "generate_report.py"
                    subprocess.run([sys.executable, str(report_script_path)], check=True)
                    
                    # Archive the trigger file
                    archive_dir = Path("/Users/flyngcoq/AI_Project/Archive")
                    archive_dir.mkdir(exist_ok=True)
                    shutil.move(event.src_path, str(archive_dir / Path(event.src_path).name))
                    print("✅ 주간 보고서 생성 파이프라인 완료!\n")
                    return

                script_path = Path(__file__).parent / "process_markdowns.py"
                subprocess.run([sys.executable, str(script_path)], check=True)
                print("✅ AI 처리 완료!\n")
            except Exception as e:
                print(f"❌ 파이프라인 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    # Ensure Inbox exists
    Path(INBOX_DIR).mkdir(parents=True, exist_ok=True)
    
    event_handler = InboxHandler()
    observer = Observer()
    observer.schedule(event_handler, INBOX_DIR, recursive=False)
    observer.start()
    
    print(f"👀 실시간 감시 시작: {INBOX_DIR}")
    print("이제 Inbox에 파일을 툭 던지기만 하면 AI가 자동으로 처리합니다! (종료: Ctrl+C)")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
