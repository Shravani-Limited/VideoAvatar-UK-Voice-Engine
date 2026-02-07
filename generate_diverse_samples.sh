#!/bin/bash
export PYTHONPATH=/home/ubuntu/regional_voice_engine/f5_tts_repo/src
cd /home/ubuntu/regional_voice_engine/f5_tts_repo/src/f5_tts/infer/
OUTPUT_DIR="/home/ubuntu/regional_voice_engine/diverse_samples_$(date +%Y%m%d_%H%M)"
mkdir -p "$OUTPUT_DIR"

# Diverse scripts for different contexts
declare -A SCRIPTS
SCRIPTS[business]="Good morning, I'm calling to discuss our quarterly performance. Revenue has increased by fifteen percent, and we're expanding into three new markets this year."
SCRIPTS[casual]="Hey! Just wanted to check in and see how you're doing. We should grab coffee sometime next week if you're free."
SCRIPTS[technical]="The server migration is scheduled for Saturday at two AM. We'll need to update the DNS records and verify all API endpoints are functioning correctly."
SCRIPTS[storytelling]="It was a cold winter morning when she first arrived in London. The fog hung thick over the Thames, and the city seemed to whisper secrets from centuries past."
SCRIPTS[educational]="Today we'll explore the fundamentals of machine learning. Neural networks are computational models inspired by the human brain's structure and function."
SCRIPTS[customer_service]="Thank you for contacting our support team. I understand you're experiencing difficulties with your account. Let me help you resolve this issue right away."

# Regional references with diverse scripts
declare -A REFS
REFS[southern_female]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p225/p225_001.wav|Please call Stella."
REFS[northern_female]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p236/p236_002.wav|Ask her to bring these things with her from the store."
REFS[scottish_male]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p237/p237_002.wav|Ask her to bring these things with her from the store."
REFS[irish_male]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p245/p245_001.wav|Please call Stella."
REFS[welsh_female]="/home/ubuntu/regional_voice_engine/datasets/vctk/VCTK-Corpus/wav48/p253/p253_001.wav|Please call Stella."

# Generate samples for each region with each script type
for REGION in "${!REFS[@]}"; do
    IFS='|' read -r REF_AUDIO REF_TEXT <<< "${REFS[$REGION]}"
    
    for SCRIPT_TYPE in "${!SCRIPTS[@]}"; do
        GEN_TEXT="${SCRIPTS[$SCRIPT_TYPE]}"
        OUTPUT_FILE="${REGION}_${SCRIPT_TYPE}.wav"
        
        echo "🚀 Generating $OUTPUT_FILE..."
        /home/ubuntu/regional_voice_engine/venv/bin/python3 infer_cli.py \
            --model train_uk_model \
            --ckpt_file /home/ubuntu/regional_voice_engine/f5_tts_repo/ckpts/uk_regional/model_last.pt \
            --vocab_file /home/ubuntu/regional_voice_engine/datasets/uk/arrow_data/vocab.txt \
            --ref_audio "$REF_AUDIO" \
            --ref_text "$REF_TEXT" \
            --gen_text "$GEN_TEXT" \
            --output_dir "$OUTPUT_DIR" \
            --device cpu \
            --speed 1.0 \
            --cfg_strength 2.0
        mv "$OUTPUT_DIR/infer_cli_basic.wav" "$OUTPUT_DIR/${OUTPUT_FILE}"
    done
done

echo "✅ Diverse sample generation complete. Results in $OUTPUT_DIR"
