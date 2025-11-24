#!/bin/bash

# AI Server Auto-Start Script with Qwen2.5-7B
# Automatically selects available GPU (prefers GPU 2)

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/ai_server.log"
PID_FILE="$WORK_DIR/ai_server/ai_server.pid"
PORT=4005
GPU_THRESHOLD=80
MODEL="qwen25-7b"
PREFERRED_GPU=2  # Prefer GPU 2 first

cd "$WORK_DIR"

echo "[$(date)] Starting AI server with Qwen2.5-7B and smart GPU selection..."

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

# Select single GPU: prefer GPU 2, then any available GPU
GPU_LIST=""
HAS_PREFERRED_GPU=false
FIRST_AVAILABLE_GPU=""

# Check if preferred GPU is available
for gpu in $AVAILABLE_GPUS; do
    if [ "$gpu" = "$PREFERRED_GPU" ]; then
        HAS_PREFERRED_GPU=true
        break
    fi
    # Store first available GPU as fallback
    if [ -z "$FIRST_AVAILABLE_GPU" ]; then
        FIRST_AVAILABLE_GPU="$gpu"
    fi
done

# Select GPU (only ONE GPU at a time)
if [ "$HAS_PREFERRED_GPU" = true ]; then
    GPU_LIST="$PREFERRED_GPU"
    echo "[$(date)] ✅ Using preferred GPU $PREFERRED_GPU (utilization < ${GPU_THRESHOLD}%)"
elif [ -n "$FIRST_AVAILABLE_GPU" ]; then
    GPU_LIST="$FIRST_AVAILABLE_GPU"
    echo "[$(date)] ✅ Preferred GPU $PREFERRED_GPU busy, using GPU $FIRST_AVAILABLE_GPU instead"
else
    # No GPU available at all
    echo "[$(date)] ❌ ERROR: All GPUs are busy (utilization >= ${GPU_THRESHOLD}%)"
    echo "[$(date)] Will retry at next scheduled time"
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

# Start new server with selected GPUs and Qwen2.5-7B model
echo "[$(date)] Starting AI server with Qwen2.5-7B on GPUs: $GPU_LIST"
CUDA_VISIBLE_DEVICES=$GPU_LIST nohup /home/i0179/bin/python3 ai_server/qwen3_4b_lowmem.py --port $PORT --model $MODEL > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "[$(date)] AI server started with PID: $NEW_PID"
echo "[$(date)] Model: Qwen2.5-7B"
echo "[$(date)] Using GPUs: $GPU_LIST"
echo "[$(date)] Log file: $LOG_FILE"

# Wait a bit and check if server is still running
sleep 5
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "[$(date)] ✅ AI server (Qwen2.5-7B) is running successfully!"
    exit 0
else
    echo "[$(date)] ❌ AI server failed to start. Check log: $LOG_FILE"
    exit 1
fi
