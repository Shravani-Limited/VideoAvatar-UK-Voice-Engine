#!/bin/bash
export PYTHONPATH=/home/ubuntu/regional_voice_engine/f5_tts_repo/src
VENV_PYTHON="/home/ubuntu/regional_voice_engine/venv/bin/python3"
USER_DIR="/home/ubuntu/regional_voice_engine/user_samples"
INPUT_M4A="$USER_DIR/harish_ref.m4a"
WAV_24K="$USER_DIR/harish_ref_24k.wav"

echo "🔄 Converting Harish's voice sample to WAV..."
ffmpeg -i "$INPUT_M4A" -ac 1 -ar 24000 "$WAV_24K" -y

echo "📝 Transcribing voice sample using Whisper..."
# We use the 'base' model for speed but decent accuracy
$VENV_PYTHON -c "
import whisper
import os
model = whisper.load_model('base')
result = model.transcribe('$WAV_24K')
text = result['text'].strip()
with open('$USER_DIR/transcription.txt', 'w') as f:
    f.write(text)
print(text)
"

REF_TEXT=$(cat "$USER_DIR/transcription.txt")

echo "✅ Transcription: '$REF_TEXT'"

GEN_TEXT="Hi, I am Harish Agawane, your AI avatar. This voice you're hearing is a digital clone of my own speech, processed through Shravani Limited's regional voice engine. It's now possible to scale my presence globally while keeping my authentic identity."

OUTPUT_DIR="/home/ubuntu/regional_voice_engine/harish_cloned_$(date +%Y%m%d_%H%M)"
mkdir -p "$OUTPUT_DIR"

echo "🚀 Generating cloned voice sample..."
cd /home/ubuntu/regional_voice_engine/f5_tts_repo/src/f5_tts/infer/
$VENV_PYTHON infer_cli.py \
    --model train_uk_model \
    --ckpt_file /home/ubuntu/regional_voice_engine/f5_tts_repo/ckpts/uk_regional/model_last.pt \
    --vocab_file /home/ubuntu/regional_voice_engine/datasets/uk/arrow_data/vocab.txt \
    --ref_audio "$WAV_24K" \
    --ref_text "$REF_TEXT" \
    --gen_text "$GEN_TEXT" \
    --output_dir "$OUTPUT_DIR" \
    --device cuda \
    --speed 1.0 \
    --cfg_strength 2.0

mv "$OUTPUT_DIR/infer_cli_basic.wav" "$OUTPUT_DIR/harish_uk_clone.wav"

echo "✨ Harish's voice clone is ready at $OUTPUT_DIR/harish_uk_clone.wav"
