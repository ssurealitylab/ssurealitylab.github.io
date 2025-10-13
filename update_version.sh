#!/bin/bash

# Get git information
BUILD_NUMBER=$(git rev-list --count HEAD 2>/dev/null || echo "0")
COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
LAST_UPDATED=$(date +%Y-%m-%d)

# Update version.yml
cat > _data/version.yml <<EOF
build_number: $BUILD_NUMBER
commit_hash: $COMMIT_HASH
version: v$BUILD_NUMBER
last_updated: $LAST_UPDATED
EOF

echo "Version updated to v$BUILD_NUMBER (Build #$BUILD_NUMBER, commit: $COMMIT_HASH)"
