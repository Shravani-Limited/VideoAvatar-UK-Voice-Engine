#!/bin/bash
export PYTHONPATH=/home/ubuntu/regional_voice_engine/f5_tts_repo/src
VENV_PYTHON="/home/ubuntu/regional_voice_engine/venv/bin/python3"

# Path to a London Male Speaker (p243) from our VCTK dataset
LONDON_REF="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p243/p243_001.wav"
LONDON_TEXT="Please call Stella."

GEN_TEXT="Hi, I am Harish Agawane. We are testing the London male voice capability of the VideoAvatar.ai engine. This model identifies the specific cadence of the London accent and delivers it with professional clarity."

OUTPUT_DIR="/home/ubuntu/regional_voice_engine/london_male_test"
mkdir -p "$OUTPUT_DIR"

echo "🚀 Generating London Male voice..."
cd /home/ubuntu/regional_voice_engine/f5_tts_repo/src/f5_tts/infer/
$VENV_PYTHON infer_cli.py \
    --model train_uk_model \
    --ckpt_file /home/ubuntu/regional_voice_engine/f5_tts_repo/ckpts/uk_regional/model_last.pt \
    --vocab_file /home/ubuntu/regional_voice_engine/datasets/uk/arrow_data/vocab.txt \
    --ref_audio "$LONDON_REF" \
    --ref_text "$LONDON_TEXT" \
    --gen_text "$GEN_TEXT" \
    --output_dir "$OUTPUT_DIR" \
    --device cuda \
    --speed 1.0 \
    --cfg_strength 2.0

mv "$OUTPUT_DIR/infer_cli_basic.wav" "$OUTPUT_DIR/london_male_sample.wav"
echo "✨ London voice sample ready at $OUTPUT_DIR/london_male_sample.wav"
