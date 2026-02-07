#!/bin/bash
export PYTHONPATH=/home/ubuntu/regional_voice_engine/f5_tts_repo/src
cd /home/ubuntu/regional_voice_engine/f5_tts_repo/src/f5_tts/infer/
OUTPUT_DIR="/home/ubuntu/regional_voice_engine/perfection_suite_$(date +%Y%m%d_%H%M)"
mkdir -p "$OUTPUT_DIR"

GEN_TEXT="Hi, I am Harish Agawane, Founder of VideoAvatar.ai. We are building the most natural regional AI voices in the world. Our UK model is now mastering the unique sounds of the North, the Midlands, and the West Country."

declare -A REFS
# Categories: Southern, Northern, Scottish, Irish, Welsh
REFS[southern_female]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p225/p225_001.wav|Please call Stella."
REFS[northern_female]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p236/p236_002.wav|Ask her to bring these things with her from the store."
REFS[scottish_male]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p237/p237_002.wav|Ask her to bring these things with her from the store."
REFS[irish_male]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p245/p245_001.wav|Please call Stella."
REFS[welsh_female]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p253/p253_001.wav|Please call Stella."

for KEY in "${!REFS[@]}"; do
    IFS='|' read -r REF_AUDIO REF_TEXT <<< "${REFS[$KEY]}"
    echo "🚀 Generating $KEY..."
    /home/ubuntu/regional_voice_engine/venv/bin/python3 infer_cli.py \
        --model train_uk_model \
        --ckpt_file /home/ubuntu/regional_voice_engine/f5_tts_repo/ckpts/uk_regional/model_last.pt \
        --vocab_file /home/ubuntu/regional_voice_engine/datasets/uk/arrow_data/vocab.txt \
        --ref_audio "$REF_AUDIO" \
        --ref_text "$REF_TEXT" \
        --gen_text "$GEN_TEXT" \
        --output_dir "$OUTPUT_DIR" \
        --device cpu \
        --speed 0.9 \
        --cfg_strength 2.0
    mv "$OUTPUT_DIR/infer_cli_basic.wav" "$OUTPUT_DIR/${KEY}.wav"
done

echo "✅ Perfection Suite complete. Results in $OUTPUT_DIR"
