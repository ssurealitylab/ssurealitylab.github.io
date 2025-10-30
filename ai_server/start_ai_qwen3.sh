#!/bin/bash

# AI Server Auto-Start Script with Qwen3-4B
# Uses ONLY GPU 3 (requires GPU 3 utilization < 80%)

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/ai_server.log"
PID_FILE="$WORK_DIR/ai_server/ai_server.pid"
PORT=4005
GPU_THRESHOLD=80
MODEL="qwen3-4b"

cd "$WORK_DIR"

echo "[$(date)] Starting AI server with Qwen3-4B and smart GPU selection..."

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
FALLBACK_GPU=""

for gpu in $AVAILABLE_GPUS; do
    if [ "$gpu" = "3" ]; then
        HAS_GPU3=true
    elif [ -z "$FALLBACK_GPU" ]; then
        FALLBACK_GPU="$gpu"
    fi
done

# Prefer GPU 3, but use any available GPU if GPU 3 is busy
if [ "$HAS_GPU3" = true ]; then
    GPU_LIST="3"
    echo "[$(date)] Using preferred GPU 3"
elif [ -n "$FALLBACK_GPU" ]; then
    GPU_LIST="$FALLBACK_GPU"
    echo "[$(date)] GPU 3 busy, using fallback GPU $FALLBACK_GPU"
else
    # No GPU available at all
    echo "[$(date)] ERROR: No GPU available (all have utilization >= ${GPU_THRESHOLD}%)"
    echo "[$(date)] Will retry in next schedule"
    exit 1
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

# Start new server with selected GPUs and Qwen3-4B model
echo "[$(date)] Starting AI server with Qwen3-4B on GPUs: $GPU_LIST"
CUDA_VISIBLE_DEVICES=$GPU_LIST nohup /home/i0179/bin/python3 ai_server/qwen3_4b_lowmem.py --port $PORT --model $MODEL > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "[$(date)] AI server started with PID: $NEW_PID"
echo "[$(date)] Model: Qwen3-4B"
echo "[$(date)] Using GPUs: $GPU_LIST"
echo "[$(date)] Log file: $LOG_FILE"

# Wait a bit and check if server is still running
sleep 5
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "[$(date)] ✅ AI server (Qwen3-4B) is running successfully!"
    exit 0
else
    echo "[$(date)] ❌ AI server failed to start. Check log: $LOG_FILE"
    exit 1
fi
