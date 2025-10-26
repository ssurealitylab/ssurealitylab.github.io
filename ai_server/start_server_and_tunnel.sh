#!/bin/bash

# Reality Lab AI Server + Tunnel Start Script
# Korean Time (KST)

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/ai_server/server_schedule.log"

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "[$(date)] ☀️  Starting AI server + tunnel..." >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

cd "$WORK_DIR"

# Step 1: Start AI Server
echo "[$(date)] Step 1/2: Starting AI server..." >> "$LOG_FILE"
bash ai_server/start_ai_qwen3.sh >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ AI server started successfully" >> "$LOG_FILE"
else
    echo "[$(date)] ⚠️  AI server start had issues (check log)" >> "$LOG_FILE"
fi

# Wait for AI server to be ready
sleep 10

# Step 2: Start Cloudflare tunnel
echo "[$(date)] Step 2/2: Starting Cloudflare tunnel..." >> "$LOG_FILE"
bash ai_server/restart_tunnel.sh >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ Cloudflare tunnel started successfully" >> "$LOG_FILE"
else
    echo "[$(date)] ⚠️  Tunnel start had issues (check log)" >> "$LOG_FILE"
fi

echo "[$(date)] 🚀 Server + Tunnel ready!" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
