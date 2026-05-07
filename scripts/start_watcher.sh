#!/bin/bash

# Move to scripts directory
cd /Users/flyngcoq/AI_Project/scripts

# Run both the telegram bot and the inbox watcher in the background
# We will use wait so the script stays alive
python3 -u agents/telegram_bot.py &
python3 -u agents/inbox_watcher.py &

# Wait for background processes
wait
