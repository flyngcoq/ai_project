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

echo "Committing changes..."
git commit -m "Auto-sync: $(date +'%Y-%m-%d %H:%M:%S')"

echo "Pushing to origin..."
git push origin main

echo "Sync completed!"
