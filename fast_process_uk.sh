#!/bin/bash
set -e

# Define paths
DATA_ROOT="datasets/uk"
EXTRACT_DIR="datasets/uk/extracted"
PROCESSED_DIR="datasets/uk/processed"

echo "📂 Starting extraction of UK Dialects..."
mkdir -p "$EXTRACT_DIR"

# Unzip all zip files into their own folders
for zipparams in "$DATA_ROOT"/*.zip; do
    [ -e "$zipparams" ] || continue
    filename=$(basename -- "$zipparams")
    dirname="${filename%.*}"
    
    echo "   ➡️ Unzipping $filename..."
    mkdir -p "$EXTRACT_DIR/$dirname"
    # Quietly unzip, skip if already exists
    unzip -q -n "$zipparams" -d "$EXTRACT_DIR/$dirname"
done

echo "✅ Extraction complete."

echo "🔄 Starting Audio Preprocessing..."
echo "   Input: $EXTRACT_DIR"
echo "   Output: $PROCESSED_DIR"

# Run the python preprocessing script
# Ensure we are in the right venv
source venv/bin/activate
python3 preprocess_data.py \
    --input_dir "$EXTRACT_DIR" \
    --output_dir "$PROCESSED_DIR"

echo "🎉 Preprocessing Finished! Metadata is at $PROCESSED_DIR/metadata.csv"
