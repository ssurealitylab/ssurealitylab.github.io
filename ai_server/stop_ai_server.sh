#!/bin/bash

# Reality Lab AI Server Stop Script
# Korean Time (KST)

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/ai_server/server_schedule.log"

echo "[$(date)] 🌙 Stopping AI server for rest time..." >> "$LOG_FILE"

# Kill AI server
pkill -f "qwen3_4b_lowmem.py"

if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ AI server stopped successfully" >> "$LOG_FILE"
else
    echo "[$(date)] ⚠️  No AI server process found" >> "$LOG_FILE"
fi

# Kill Cloudflare tunnel
pkill -f "cloudflared tunnel"

if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ Cloudflare tunnel stopped" >> "$LOG_FILE"
else
    echo "[$(date)] ⚠️  No tunnel process found" >> "$LOG_FILE"
fi

echo "[$(date)] 💤 Rest time started (4 AM - 8 AM KST)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
