import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import sys
import datetime
import subprocess
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Use core modules
from core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, VAULT_DIR, INBOX_DIR
from core.llm_client import generate_with_ollama
from core.rag_engine import retrieve_context

def is_allowed(update: Update) -> bool:
    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "your-chat-id-here":
        return True # If not set, allow all (for initial testing to get the chat ID)
    return str(update.effective_chat.id) == str(TELEGRAM_CHAT_ID)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    
    warning_msg = ""
    # If chat ID is not configured, inform the user
    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "your-chat-id-here":
        warning_msg = (
            f"⚠️ 보안 경고: 현재 TELEGRAM_CHAT_ID가 설정되지 않았습니다.\n"
            f"당신의 Chat ID는 [{update.effective_chat.id}] 입니다.\n"
            f".env 파일에 이 ID를 입력하고 봇을 재시작하세요.\n\n"
        )
        print(f"USER CHAT ID IS: {update.effective_chat.id}")
        
    await update.message.reply_text(
        f"{warning_msg}"
        "🚀 Antigravity 대화형 AI 비서 접속 완료.\n\n"
        "이 채팅방에 메시지를 보내면 즉각적으로 AI가 답변을 제공합니다!\n"
        "자료를 수집하고 싶을 땐 `/inbox` 명령어를 사용하세요.\n\n"
        "명령어:\n"
        "/status - 시스템 및 문서 동기화 상태 확인\n"
        "/report - Confluence 주간 보고서 자동 생성\n"
        "/sync - 수동 Github 동기화 실행\n"
        "/inbox <내용> - 텍스트나 링크를 Obsidian Inbox에 자동 저장"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    
    inbox_count = len(list(INBOX_DIR.glob("*.md"))) if INBOX_DIR.exists() else 0
    fleeting_count = len(list((VAULT_DIR / "10_Fleeting_Notes").glob("*.md")))
    perm_count = len(list((VAULT_DIR / "30_Permanent_Notes").glob("*.md")))
    
    msg = (
        f"📊 시스템 상태 보고\n\n"
        f"대기 중인 Inbox 문서: {inbox_count}건\n"
        f"Fleeting Notes: {fleeting_count}건\n"
        f"Permanent Notes: {perm_count}건"
    )
    await update.message.reply_text(msg)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    
    await update.message.reply_text("⏳ 주간 보고서 생성을 시작합니다...")
    try:
        report_script = Path(__file__).parent / "generate_report.py"
        result = subprocess.run([sys.executable, str(report_script)], capture_output=True, text=True)
        if result.returncode == 0:
            await update.message.reply_text("✅ 주간 보고서가 성공적으로 생성 및 업로드되었습니다!")
        else:
            await update.message.reply_text(f"❌ 보고서 생성 실패:\n{result.stderr}")
    except Exception as e:
        await update.message.reply_text(f"❌ 오류 발생: {e}")

async def save_to_inbox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
        
    if not context.args:
        await update.message.reply_text("❌ 저장할 내용을 입력해주세요. (예: `/inbox 저장할 텍스트`)")
        return
        
    text = " ".join(context.args)
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"Telegram_{timestamp}.md"
    file_path = INBOX_DIR / file_name
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
        
    context.user_data['last_inbox_time'] = datetime.datetime.now()
    context.user_data['last_inbox_file'] = file_path
        
    await update.message.reply_text(f"📥 Inbox에 저장되었습니다.\n`{file_name}`\n곧 지식 그래프 요약 파이프라인이 구동됩니다.")

async def sync(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    
    await update.message.reply_text("⏳ Github 동기화를 시작합니다...")
    try:
        sync_script = VAULT_DIR / "sync.sh"
        subprocess.run(["bash", str(sync_script)], cwd=str(VAULT_DIR), check=True)
        await update.message.reply_text("✅ 동기화 완료!")
    except Exception as e:
        await update.message.reply_text(f"❌ 동기화 실패: {e}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
        
    photo = update.message.photo[-1] # Get the largest version
    file = await context.bot.get_file(photo.file_id)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"Telegram_Photo_{timestamp}.jpg"
    file_path = INBOX_DIR / file_name
    
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    await file.download_to_drive(custom_path=str(file_path))
    
    caption = update.message.caption
    if caption:
        md_path = file_path.with_suffix(".md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"Caption from Telegram: {caption}\n\n![[{file_name}]]")
            
    await update.message.reply_text(f"📸 이미지가 Inbox에 저장되었습니다.\n`{file_name}`\n{ '캡션과 함께 ' if caption else '' }AI가 곧 분석을 시작합니다.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
        
    doc = update.message.document
    file = await context.bot.get_file(doc.file_id)
    
    # Use original filename
    original_name = doc.file_name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{original_name}"
    
    file_path = INBOX_DIR / file_name
    
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    await file.download_to_drive(custom_path=str(file_path))
    
    # Handle caption as a companion markdown file
    caption = update.message.caption
    if caption:
        md_name = f"{timestamp}_{Path(original_name).stem}.md"
        md_path = INBOX_DIR / md_name
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"Document Caption: {caption}\n\nRelated File: [[{file_name}]]")
            
    await update.message.reply_text(f"📁 파일이 Inbox에 저장되었습니다.\n`{file_name}`\n{ '캡션과 함께 ' if caption else '' }곧 파이프라인에서 분석을 시작합니다.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[{datetime.datetime.now()}] Received message from {update.effective_chat.id}: {update.message.text}")
    if not is_allowed(update):
        print(f"Unauthorized access attempt from {update.effective_chat.id}")
        return

    text = update.message.text
    if not text:
        return
        
    # Check if this is a continuation of a split /inbox message
    last_inbox_time = context.user_data.get('last_inbox_time')
    if last_inbox_time and (datetime.datetime.now() - last_inbox_time).total_seconds() < 5:
        last_inbox_file = context.user_data.get('last_inbox_file')
        if last_inbox_file and last_inbox_file.exists():
            with open(last_inbox_file, "a", encoding="utf-8") as f:
                f.write(text)
            context.user_data['last_inbox_time'] = datetime.datetime.now()
            return
            
    # Start Thinking
    status_msg = await update.message.reply_text("🤔 생각 중...")
    
    try:
        from core.orchestrator import stream_orchestrate
        from core.rag_engine import retrieve_context
        
        # Initialize/Retrieve History
        if 'history' not in context.user_data:
            context.user_data['history'] = []
            
        history = context.user_data['history']
        
        context_data = retrieve_context(text)
        
        full_response = ""
        chunk_counter = 0
        
        # Stream the orchestration with history
        print(f"[{datetime.datetime.now()}] Starting orchestration...")
        for chunk in stream_orchestrate(text, context_data, history):
            full_response += chunk
            chunk_counter += 1
            
            if chunk_counter % 5 == 0:
                try:
                    await status_msg.edit_text(full_response + " ▌")
                except Exception as e:
                    print(f"Edit error: {e}")
        
        if full_response:
            print(f"[{datetime.datetime.now()}] Response complete. Length: {len(full_response)}")
            await status_msg.edit_text(full_response)
            # Update History (Keep last 10 messages)
            history.append({"role": "user", "content": text})
            history.append({"role": "assistant", "content": full_response})
            context.user_data['history'] = history[-10:]
        else:
            await status_msg.edit_text("⚠️ 응답을 생성하지 못했습니다.")
            
    except Exception as e:
        await status_msg.edit_text(f"❌ AI 생성 오류 발생:\n{str(e)}")

def main():
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your-bot-token-here":
        print("Error: TELEGRAM_BOT_TOKEN is not set correctly in .env")
        sys.exit(1)
        
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("sync", sync))
    app.add_handler(CommandHandler("inbox", save_to_inbox))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Telegram Bot Started. Waiting for messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
