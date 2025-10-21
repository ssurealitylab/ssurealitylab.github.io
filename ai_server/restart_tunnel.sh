#!/bin/bash

# Cloudflare Tunnel Auto-Restart Script
# This script restarts the cloudflare tunnel and updates the chatbot URL

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/cloudflare_tunnel.log"
CHATBOT_FILE="$WORK_DIR/_includes/chatbot.html"
PID_FILE="$WORK_DIR/ai_server/cloudflared.pid"

cd "$WORK_DIR"

echo "[$(date)] Starting Cloudflare Tunnel restart..." >> "$LOG_FILE"

# Kill existing cloudflared process
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "[$(date)] Killing old cloudflared process (PID: $OLD_PID)" >> "$LOG_FILE"
        kill $OLD_PID
        sleep 2
    fi
fi

# Kill any remaining cloudflared processes
pkill -f "cloudflared tunnel"
sleep 2

# Start new cloudflared tunnel
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "[$(date)] Starting new cloudflared tunnel..." >> "$LOG_FILE"
nohup ./ai_server/cloudflared tunnel --url http://localhost:4005 >> "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

# Wait for tunnel to initialize
echo "[$(date)] Waiting for tunnel to initialize..." >> "$LOG_FILE"
sleep 5

# Extract new URL from log (get the LAST/newest one)
NEW_URL=$(grep -oP 'https://[a-z-]+\.trycloudflare\.com' "$LOG_FILE" | tail -1)

if [ -z "$NEW_URL" ]; then
    echo "[$(date)] ERROR: Failed to get new tunnel URL!" >> "$LOG_FILE"
    exit 1
fi

echo "[$(date)] New tunnel URL: $NEW_URL" >> "$LOG_FILE"

# Get old URL from chatbot.html
OLD_URL=$(grep -oP "DIRECT_AI_SERVER_URL = 'https://[a-z-]+\.trycloudflare\.com'" "$CHATBOT_FILE" | grep -oP 'https://[a-z-]+\.trycloudflare\.com')

if [ "$OLD_URL" == "$NEW_URL" ]; then
    echo "[$(date)] URL unchanged, no update needed" >> "$LOG_FILE"
    exit 0
fi

echo "[$(date)] Old URL: $OLD_URL" >> "$LOG_FILE"
echo "[$(date)] Updating chatbot.html..." >> "$LOG_FILE"

# Update chatbot.html with new URL
sed -i "s|DIRECT_AI_SERVER_URL = '$OLD_URL'|DIRECT_AI_SERVER_URL = '$NEW_URL'|g" "$CHATBOT_FILE"

# Verify update
if grep -q "$NEW_URL" "$CHATBOT_FILE"; then
    echo "[$(date)] chatbot.html updated successfully" >> "$LOG_FILE"
else
    echo "[$(date)] ERROR: Failed to update chatbot.html!" >> "$LOG_FILE"
    exit 1
fi

# Commit and push changes
echo "[$(date)] Committing changes to git..." >> "$LOG_FILE"
git add "$CHATBOT_FILE"
git commit -m "Auto-update Cloudflare Tunnel URL to $NEW_URL

🤖 Auto-updated by tunnel restart script

Co-Authored-By: Claude <noreply@anthropic.com>" >> "$LOG_FILE" 2>&1

# Update version
./update_version.sh >> "$LOG_FILE" 2>&1
git add _data/version.yml
git commit -m "Update version (tunnel restart)" >> "$LOG_FILE" 2>&1

# Push to GitHub
echo "[$(date)] Pushing to GitHub..." >> "$LOG_FILE"
git push origin main >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] Successfully pushed to GitHub!" >> "$LOG_FILE"
else
    echo "[$(date)] WARNING: Failed to push to GitHub" >> "$LOG_FILE"
fi

echo "[$(date)] Tunnel restart completed successfully!" >> "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"
