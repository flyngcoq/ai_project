#!/bin/bash
# Simple script to sync Obsidian Vault with Github

# Move to the directory where this script is located
cd "$(dirname "$0")"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Git repository is not initialized. Please run 'git init' first."
    exit 1
fi

echo "Staging changes..."
git add .

echo "Committing local changes (if any)..."
git commit -m "Auto-sync: $(date +'%Y-%m-%d %H:%M:%S')" || echo "No local changes to commit."

echo "Pulling latest changes from Github..."
git pull origin main --rebase

echo "Pushing everything to origin..."
git push origin main

echo "Sync completed!"
