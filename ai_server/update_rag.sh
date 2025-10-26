#!/bin/bash

# Reality Lab RAG Auto-Update Script
# Crawls website, rebuilds vector database, and restarts AI server

WORK_DIR="/home/i0179/Realitylab-site"
LOG_FILE="$WORK_DIR/ai_server/rag_update.log"

cd "$WORK_DIR"

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "[$(date)] Starting RAG Update..." >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Step 1: Crawl website
echo "[$(date)] Step 1/4: Crawling website..." >> "$LOG_FILE"
python3 ai_server/crawl_website.py >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] ERROR: Website crawling failed!" >> "$LOG_FILE"
    exit 1
fi
echo "[$(date)] ✅ Website crawled successfully" >> "$LOG_FILE"

# Step 2: Build vector database
echo "[$(date)] Step 2/4: Building vector database..." >> "$LOG_FILE"
python3 ai_server/build_vector_db.py >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] ERROR: Vector DB build failed!" >> "$LOG_FILE"
    exit 1
fi
echo "[$(date)] ✅ Vector database built successfully" >> "$LOG_FILE"

# Step 3: Restart AI server to load new vector DB
echo "[$(date)] Step 3/4: Restarting AI server..." >> "$LOG_FILE"

# Kill old AI server
pkill -f "qwen3_4b_lowmem.py"
sleep 3

# Start new AI server
bash ai_server/start_ai_qwen3.sh >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] WARNING: AI server restart had issues (check log)" >> "$LOG_FILE"
else
    echo "[$(date)] ✅ AI server restarted successfully" >> "$LOG_FILE"
fi

# Step 4: Log completion
echo "[$(date)] Step 4/4: RAG update complete!" >> "$LOG_FILE"

# Summary
DOCS_COUNT=$(python3 -c "import json; f=open('ai_server/knowledge_base.json'); data=json.load(f); print(len(data)); f.close()")
VECTOR_COUNT=$(python3 -c "import json; f=open('ai_server/vector_db/config.json'); data=json.load(f); print(data['num_documents']); f.close()")

echo "" >> "$LOG_FILE"
echo "Summary:" >> "$LOG_FILE"
echo "  Knowledge base documents: $DOCS_COUNT" >> "$LOG_FILE"
echo "  Vector database size: $VECTOR_COUNT vectors" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "[$(date)] ✅ RAG Update Completed Successfully!" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
