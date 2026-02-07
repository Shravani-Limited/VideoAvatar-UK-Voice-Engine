#!/bin/bash
set -e

# Define paths
REGIONAL_ROOT="/home/ubuntu/regional_voice_engine"
VCTK_ROOT="$REGIONAL_ROOT/datasets/vctk"

# 1. Extract VCTK
cd "$VCTK_ROOT"
if [ ! -d "VCTK-Corpus" ]; then
    echo "📦 Extracting VCTK-Corpus..."
    tar -xzf VCTK-Corpus.tar.gz
else
    echo "✅ VCTK-Corpus already extracted."
fi

# 2. Filter and generate metadata.csv
cd "$REGIONAL_ROOT"
source venv/bin/activate
echo "🎯 Filtering for UK Regional speakers..."
python3 process_vctk_regional.py

# 3. Convert to Arrow format (F5-TTS preparation)
echo "🔄 Converting to Arrow format..."
export PYTHONPATH="$REGIONAL_ROOT/f5_tts_repo/src"
python3 "$REGIONAL_ROOT/f5_tts_repo/src/f5_tts/train/datasets/prepare_csv_wavs.py" \
    "$REGIONAL_ROOT/datasets/uk/processed/metadata.csv" \
    "$REGIONAL_ROOT/datasets/uk/arrow_data"

# 4. Wipe previous non-compliant checkpoints
echo "🧹 Wiping non-compliant checkpoints..."
# We keep pretrained_model.safetensors as a starting point if needed, 
# but we effectively restart the finetuning from there with new data.
rm -f "$REGIONAL_ROOT/f5_tts_repo/ckpts/uk_regional/model_*.pt"
rm -f "$REGIONAL_ROOT/f5_tts_repo/ckpts/uk_regional/model_last.pt"

# 5. Relaunch Training (on all 4 GPUs)
echo "🚀 Relaunching Training on 4 GPUs..."
cd "$REGIONAL_ROOT/f5_tts_repo/src/f5_tts/train"
# Ensure accelerate is configured or use default
CUDA_VISIBLE_DEVICES=0,1,2,3 /home/ubuntu/regional_voice_engine/venv/bin/accelerate launch \
    --main_process_port 29515 \
    --num_processes 4 \
    train.py --config-name train_uk_model > "$REGIONAL_ROOT/train_uk_compliant.log" 2>&1 &

echo "✨ UK Compliance Relaunch complete!"
echo "📡 Training log: $REGIONAL_ROOT/train_uk_compliant.log"
