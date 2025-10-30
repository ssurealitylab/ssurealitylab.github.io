#!/bin/bash

# GPU Monitoring & Auto-Switch Script
# Checks current GPU usage every hour and switches to available GPU if needed

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/ai_server/gpu_monitor.log"
PID_FILE="$WORK_DIR/ai_server/ai_server.pid"
GPU_FILE="$WORK_DIR/ai_server/current_gpu.txt"
PORT=4005
GPU_THRESHOLD=30  # Switch if current GPU > 30%

cd "$WORK_DIR"

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "[$(date)] 🔍 GPU Monitoring Check" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Check if AI server is running
if [ ! -f "$PID_FILE" ]; then
    echo "[$(date)] ⚠️  AI server not running (no PID file)" >> "$LOG_FILE"
    exit 0
fi

SERVER_PID=$(cat "$PID_FILE")
if ! ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "[$(date)] ⚠️  AI server not running (PID $SERVER_PID not found)" >> "$LOG_FILE"
    exit 0
fi

# Get current GPU from file or environment
CURRENT_GPU=""
if [ -f "$GPU_FILE" ]; then
    CURRENT_GPU=$(cat "$GPU_FILE")
else
    # Try to detect from process
    CURRENT_GPU=$(ps eww -p $SERVER_PID | grep -oP 'CUDA_VISIBLE_DEVICES=\K[0-9]+' | head -1)
    if [ -z "$CURRENT_GPU" ]; then
        echo "[$(date)] ⚠️  Cannot detect current GPU" >> "$LOG_FILE"
        exit 0
    fi
    echo "$CURRENT_GPU" > "$GPU_FILE"
fi

echo "[$(date)] Current GPU: $CURRENT_GPU" >> "$LOG_FILE"

# Get current GPU utilization
CURRENT_GPU_UTIL=$(nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits | grep "^$CURRENT_GPU," | cut -d',' -f2 | tr -d ' ')

if [ -z "$CURRENT_GPU_UTIL" ]; then
    echo "[$(date)] ⚠️  Cannot read GPU utilization" >> "$LOG_FILE"
    exit 0
fi

echo "[$(date)] Current GPU $CURRENT_GPU utilization: ${CURRENT_GPU_UTIL}%" >> "$LOG_FILE"

# Check if current GPU is still good (< 30%)
if [ "$CURRENT_GPU_UTIL" -lt "$GPU_THRESHOLD" ]; then
    echo "[$(date)] ✅ Current GPU is healthy (${CURRENT_GPU_UTIL}% < ${GPU_THRESHOLD}%), no action needed" >> "$LOG_FILE"
    exit 0
fi

# Current GPU is overloaded (>= 30%), search for better GPU
echo "[$(date)] ⚠️  Current GPU overloaded (${CURRENT_GPU_UTIL}% >= ${GPU_THRESHOLD}%), searching for available GPU..." >> "$LOG_FILE"

# Find available GPU (utilization < 30%)
AVAILABLE_GPU=""
nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits | while read line; do
    gpu_id=$(echo $line | cut -d',' -f1 | tr -d ' ')
    utilization=$(echo $line | cut -d',' -f2 | tr -d ' ')

    if [ "$utilization" -lt "$GPU_THRESHOLD" ] && [ "$gpu_id" != "$CURRENT_GPU" ]; then
        echo "$gpu_id"
        break
    fi
done > /tmp/available_gpu_temp.txt

AVAILABLE_GPU=$(cat /tmp/available_gpu_temp.txt)
rm -f /tmp/available_gpu_temp.txt

if [ -z "$AVAILABLE_GPU" ]; then
    echo "[$(date)] ❌ No available GPU found (all GPUs >= ${GPU_THRESHOLD}%), keeping current GPU" >> "$LOG_FILE"
    exit 0
fi

echo "[$(date)] ✅ Found available GPU: $AVAILABLE_GPU" >> "$LOG_FILE"

# Switch to new GPU
echo "[$(date)] 🔄 Switching AI server from GPU $CURRENT_GPU to GPU $AVAILABLE_GPU..." >> "$LOG_FILE"

# Kill current server
echo "[$(date)] Stopping current AI server (PID: $SERVER_PID)..." >> "$LOG_FILE"
kill $SERVER_PID
sleep 3

# Make sure it's stopped
pkill -f "qwen3_4b_lowmem.py"
sleep 2

# Start on new GPU
echo "[$(date)] Starting AI server on GPU $AVAILABLE_GPU..." >> "$LOG_FILE"
CUDA_VISIBLE_DEVICES=$AVAILABLE_GPU nohup /home/i0179/bin/python3 ai_server/qwen3_4b_lowmem.py --port $PORT --model qwen3-4b > "$WORK_DIR/ai_server.log" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"
echo $AVAILABLE_GPU > "$GPU_FILE"

echo "[$(date)] AI server started with PID: $NEW_PID on GPU $AVAILABLE_GPU" >> "$LOG_FILE"

# Wait for server to initialize (90 seconds for model loading)
echo "[$(date)] Waiting 90 seconds for model to load..." >> "$LOG_FILE"
sleep 90

# Verify server is running
if ! ps -p $NEW_PID > /dev/null 2>&1; then
    echo "[$(date)] ❌ AI server failed to start!" >> "$LOG_FILE"
    exit 1
fi

# Test server connection
echo "[$(date)] Testing server connection..." >> "$LOG_FILE"
TEST_RESPONSE=$(curl -s -X POST http://localhost:$PORT/chat \
    -H "Content-Type: application/json" \
    -d '{"question":"안녕하세요"}' \
    --max-time 60)

if [ $? -eq 0 ] && echo "$TEST_RESPONSE" | grep -q "response"; then
    echo "[$(date)] ✅ AI server successfully switched to GPU $AVAILABLE_GPU and verified!" >> "$LOG_FILE"
    echo "[$(date)] Test response received successfully" >> "$LOG_FILE"
else
    echo "[$(date)] ⚠️  Server started but verification failed" >> "$LOG_FILE"
fi

echo "========================================" >> "$LOG_FILE"
