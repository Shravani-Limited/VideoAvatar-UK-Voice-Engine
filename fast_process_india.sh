#!/bin/bash
set -e

# Define paths
DATA_ROOT="regional_voice_engine/datasets/india"
EXTRACT_DIR="regional_voice_engine/datasets/india/extracted"
PROCESSED_DIR="regional_voice_engine/datasets/india/processed"

echo "📂 Starting extraction of Indian Languages..."
mkdir -p "$EXTRACT_DIR"

# Unzip all zip/tar.gz files
# OpenSLR India often uses .zip for south languages and .tar.gz for others
for zipparams in "$DATA_ROOT"/*.zip "$DATA_ROOT"/*.tar.gz; do
    [ -e "$zipparams" ] || continue
    filename=$(basename -- "$zipparams")
    dirname="${filename%.*}"
    # Remove .tar if it was .tar.gz
    dirname="${dirname%.tar}"
    
    target_path="$EXTRACT_DIR/$dirname"
    echo "   ➡️ Extracting $filename to $target_path..."
    mkdir -p "$target_path"
    
    if [[ "$zipparams" == *.zip ]]; then
        unzip -q -n "$zipparams" -d "$target_path"
    elif [[ "$zipparams" == *.tar.gz ]]; then
        tar -xzf "$zipparams" -C "$target_path"
    fi
done

echo "✅ Extraction complete."

echo "🔄 Starting Audio Preprocessing (India)..."
echo "   Input: $EXTRACT_DIR"
echo "   Output: $PROCESSED_DIR"

source regional_voice_engine/venv/bin/activate
python3 regional_voice_engine/preprocess_data.py \
    --input_dir "$EXTRACT_DIR" \
    --output_dir "$PROCESSED_DIR"

echo "🎉 Preprocessing Finished! Metadata is at $PROCESSED_DIR/metadata.csv"
