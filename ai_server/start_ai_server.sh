#!/bin/bash

# AI Server Auto-Start Script with Smart GPU Selection
# Prioritizes GPU 3, adds other GPUs if utilization < 80%

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/ai_server.log"
PID_FILE="$WORK_DIR/ai_server/ai_server.pid"
PORT=4005
GPU_THRESHOLD=80

cd "$WORK_DIR"

echo "[$(date)] Starting AI server with smart GPU selection..."

# Function to get available GPUs
get_available_gpus() {
    # Get GPU info: index, utilization
    nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits | while read line; do
        gpu_id=$(echo $line | cut -d',' -f1 | tr -d ' ')
        utilization=$(echo $line | cut -d',' -f2 | tr -d ' ')

        # Check if utilization is below threshold
        if [ "$utilization" -lt "$GPU_THRESHOLD" ]; then
            echo "$gpu_id"
        fi
    done
}

# Get available GPUs
AVAILABLE_GPUS=$(get_available_gpus)

if [ -z "$AVAILABLE_GPUS" ]; then
    echo "[$(date)] ERROR: No GPU with utilization < ${GPU_THRESHOLD}% available!"
    exit 1
fi

# Convert to comma-separated list, prioritizing GPU 3
GPU_LIST=""
HAS_GPU3=false

for gpu in $AVAILABLE_GPUS; do
    if [ "$gpu" = "3" ]; then
        HAS_GPU3=true
    fi
done

# Build GPU list with GPU 3 first if available
if [ "$HAS_GPU3" = true ]; then
    GPU_LIST="3"
    for gpu in $AVAILABLE_GPUS; do
        if [ "$gpu" != "3" ]; then
            GPU_LIST="$GPU_LIST,$gpu"
        fi
    done
else
    # GPU 3 not available, use others
    first=true
    for gpu in $AVAILABLE_GPUS; do
        if [ "$first" = true ]; then
            GPU_LIST="$gpu"
            first=false
        else
            GPU_LIST="$GPU_LIST,$gpu"
        fi
    done
fi

echo "[$(date)] Available GPUs (utilization < ${GPU_THRESHOLD}%): $GPU_LIST"

# Kill existing server if running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "[$(date)] Stopping old server (PID: $OLD_PID)..."
        kill $OLD_PID
        sleep 3
    fi
fi

# Kill any remaining python processes on port 4005
pkill -f "qwen3_4b_lowmem.py"
sleep 2

# Start new server with selected GPUs
echo "[$(date)] Starting AI server on GPUs: $GPU_LIST"
CUDA_VISIBLE_DEVICES=$GPU_LIST nohup /home/i0179/bin/python3 ai_server/qwen3_4b_lowmem.py --port $PORT > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "[$(date)] AI server started with PID: $NEW_PID"
echo "[$(date)] Using GPUs: $GPU_LIST"
echo "[$(date)] Log file: $LOG_FILE"

# Wait a bit and check if server is still running
sleep 5
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "[$(date)] ✅ AI server is running successfully!"
    exit 0
else
    echo "[$(date)] ❌ AI server failed to start. Check log: $LOG_FILE"
    exit 1
fi
