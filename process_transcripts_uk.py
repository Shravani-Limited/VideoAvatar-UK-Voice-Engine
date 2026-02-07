import os
import glob
import csv
from pathlib import Path

DATA_ROOT = "datasets/uk"
EXTRACTED_DIR = os.path.join(DATA_ROOT, "extracted")
PROCESSED_DIR = os.path.join(DATA_ROOT, "processed")
OUTPUT_CSV = os.path.join(PROCESSED_DIR, "metadata.csv")

def parse_line_index_csv(file_path):
    """Parse SLR83 line_index.csv: TRANSCRIPT_ID, FILE_ID, TEXT"""
    mapping = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    file_id = row[1].strip()
                    text = row[2].strip()
                    mapping[file_id] = text
    except Exception as e:
        print(f"Error parsing CSV {file_path}: {e}")
    return mapping

def main():
    transcript_map = {}
    
    print("🔍 Scanning for UK transcripts...")
    
    # Find all line_index.csv
    csvs = glob.glob(os.path.join(EXTRACTED_DIR, "**", "line_index.csv"), recursive=True)
    for csv_file in csvs:
        print(f"   Parsing {csv_file}...")
        m = parse_line_index_csv(csv_file)
        transcript_map.update(m)
        
    print(f"✅ Loaded {len(transcript_map)} distinct transcript IDs.")
    
    # 4. Match with processed audio
    wavs = glob.glob(os.path.join(PROCESSED_DIR, "*.wav"))
    print(f"🔍 Found {len(wavs)} processed audio files.")
    
    matches = 0
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        # Header for F5-TTS
        writer.writerow(["audio_file", "text"])
        
        for wav in wavs:
            filename = os.path.basename(wav)
            file_id = os.path.splitext(filename)[0]
            
            if file_id in transcript_map:
                text = transcript_map[file_id]
                # F5-TTS needs absolute path
                abs_path = os.path.abspath(wav)
                writer.writerow([abs_path, text])
                matches += 1

    print(f"🎉 UK Metadata generated with {matches} matched pairs.")
    print(f"   Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
