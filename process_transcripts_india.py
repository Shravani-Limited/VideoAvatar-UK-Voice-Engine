import os
import glob
import csv
from pathlib import Path

DATA_ROOT = "datasets/india"
EXTRACTED_DIR = os.path.join(DATA_ROOT, "extracted")
PROCESSED_DIR = os.path.join(DATA_ROOT, "processed")
OUTPUT_CSV = os.path.join(PROCESSED_DIR, "metadata.csv")

def parse_line_index_tsv(file_path):
    """Parse standard OpenSLR line_index.tsv"""
    mapping = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    file_id = parts[0].strip()
                    text = parts[1].strip()
                    mapping[file_id] = text
    except Exception as e:
        print(f"Error parsing TSV {file_path}: {e}")
    return mapping

def parse_transcription_txt(file_path):
    """Parse transcription.txt (often same as TSV but space or tab separated)"""
    mapping = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Try tab first
                parts = line.strip().split('\t')
                if len(parts) < 2:
                    # Try space (often first word is ID)
                    parts = line.strip().split(' ', 1)
                
                if len(parts) >= 2:
                    file_id = parts[0].strip()
                    text = parts[1].strip()
                    # Remove extenson from ID if present
                    file_id = os.path.splitext(file_id)[0]
                    mapping[file_id] = text
    except Exception as e:
        print(f"Error parsing TXT {file_path}: {e}")
    return mapping

def main():
    transcript_map = {}
    
    print("🔍 Scanning for transcripts...")
    
    # 1. Find all line_index.tsv (Gujarati, Marathi, etc.)
    tsvs = glob.glob(os.path.join(EXTRACTED_DIR, "**", "line_index.tsv"), recursive=True)
    for tsv in tsvs:
        print(f"   Parsing {tsv}...")
        m = parse_line_index_tsv(tsv)
        transcript_map.update(m)
        
    # 2. Find transcription.txt (Hindi)
    txts = glob.glob(os.path.join(EXTRACTED_DIR, "**", "transcription.txt"), recursive=True)
    for txt in txts:
        print(f"   Parsing {txt}...")
        m = parse_transcription_txt(txt)
        transcript_map.update(m)
        
    # 3. Find unique Kashmiri text files? (Skipping for V1 complexity, or try match)
    # If the text file content is the transcript, we'd need to map audio filename -> text file content.
    
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
            else:
                # Debug sample misses
                if matches == 0 and len(wavs) > 0: 
                     # Checking mostly for debugging
                     pass

    print(f"🎉 Metadata generated with {matches} matched pairs.")
    print(f"   Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
