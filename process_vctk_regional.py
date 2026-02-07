import os
import glob
import csv
from pathlib import Path

# VCTK Structure:
# VCTK-Corpus/
#   wav48/
#     p225/
#       p225_001.wav
#   txt/
#     p225/
#       p225_001.txt
#   speaker-info.txt

DATA_ROOT = "datasets/vctk/VCTK-Corpus"
OUTPUT_ROOT = "datasets/uk/processed"
OUTPUT_CSV = os.path.join(OUTPUT_ROOT, "metadata.csv")

def parse_speaker_info(file_path):
    """
    Parse speaker-info.txt
    Format: ID  AGE  GENDER  ACCENT  REGION
    Note: Some entries might skip columns or have different spacing.
    """
    speakers = {}
    if not os.path.exists(file_path):
        print(f"❌ speaker-info.txt not found at {file_path}")
        return speakers
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Skip header if first line is headers
        start_idx = 0
        if "ID" in lines[0]:
            start_idx = 1
            
        for line in lines[start_idx:]:
            parts = line.strip().split()
            if len(parts) >= 4:
                spk_id = parts[0]
                accent = parts[3]
                region = parts[4] if len(parts) > 4 else ""
                speakers[spk_id] = {"accent": accent, "region": region}
    return speakers

def main():
    if not os.path.exists(OUTPUT_ROOT):
        os.makedirs(OUTPUT_ROOT)

    speaker_info_path = os.path.join(DATA_ROOT, "speaker-info.txt")
    speakers = parse_speaker_info(speaker_info_path)
    print(f"✅ Loaded {len(speakers)} speakers from metadata.")

    # Filter for UK-like accents (English, Scottish, Welsh, Irish)
    # VCTK often uses labels like "English", "Scottish", "Welsh", "Irish", "NorthernIrish"
    uk_accents = {"English", "Scottish", "Welsh", "Irish", "NorthernIrish"}
    
    selected_speakers = {k: v for k, v in speakers.items() if v['accent'] in uk_accents}
    print(f"🎯 Found {len(selected_speakers)} UK-regional speakers.")

    # 48kHz WAVs are in wav48 directory
    wav_dir = os.path.join(DATA_ROOT, "wav48")
    txt_dir = os.path.join(DATA_ROOT, "txt")

    matches = 0
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["audio_file", "text"])
        
        for spk_id in selected_speakers:
            spk_wav_dir = os.path.join(wav_dir, f"p{spk_id}")
            spk_txt_dir = os.path.join(txt_dir, f"p{spk_id}")
            
            if not os.path.exists(spk_wav_dir):
                # VCTK sometimes uses spk_id directly if 'p' isn't prefixed
                spk_wav_dir = os.path.join(wav_dir, spk_id)
                spk_txt_dir = os.path.join(txt_dir, spk_id)

            if not os.path.exists(spk_wav_dir):
                continue
                
            wav_files = glob.glob(os.path.join(spk_wav_dir, "*.wav"))
            for wav_path in wav_files:
                file_id = os.path.splitext(os.path.basename(wav_path))[0]
                txt_path = os.path.join(spk_txt_dir, f"{file_id}.txt")
                
                if os.path.exists(txt_path):
                    with open(txt_path, 'r', encoding='utf-8') as tf:
                        text = tf.read().strip()
                        
                    # F5-TTS needs absolute path
                    abs_path = os.path.abspath(wav_path)
                    writer.writerow([abs_path, text])
                    matches += 1

    print(f"🎉 VCTK Metadata generated with {matches} matched pairs.")
    print(f"   Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
