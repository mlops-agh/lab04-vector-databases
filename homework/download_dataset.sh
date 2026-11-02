#!/usr/bin/env bash
# Result: <target_dir>/images/metadata/images.csv.gz and <target_dir>/images/small/
set -euo pipefail

TARGET_DIR="${1:-$(dirname "$0")/data}"
URL="https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-images-small.tar"

mkdir -p "$TARGET_DIR"

if [ -f "$TARGET_DIR/images/metadata/images.csv.gz" ]; then
    echo "Dataset already unpacked in $TARGET_DIR, nothing to do"
    exit 0
fi

# -C resumes an interrupted download, -f fails on HTTP errors
curl -fL -C - --progress-bar -o "$TARGET_DIR/abo-images-small.tar" "$URL"
tar -xf "$TARGET_DIR/abo-images-small.tar" -C "$TARGET_DIR"
echo "Done. Metadata file: $TARGET_DIR/images/metadata/images.csv.gz"
