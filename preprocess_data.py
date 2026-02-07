import os
import glob
import librosa
import soundfile as sf
import tqdm
import csv
import argparse

def preprocess_audio(input_dir, output_dir, sample_rate=24000):
    """
    Resample audio to target sample rate and convert to mono.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    audio_files = glob.glob(os.path.join(input_dir, "**/*.wav"), recursive=True) + \
                  glob.glob(os.path.join(input_dir, "**/*.mp3"), recursive=True) + \
                  glob.glob(os.path.join(input_dir, "**/*.flac"), recursive=True)
                  
    print(f"Found {len(audio_files)} audio files in {input_dir}")
    
    processed_files = []
    
    for file_path in tqdm.tqdm(audio_files, desc="Processing Audio"):
        try:
            # Load audio
            y, sr = librosa.load(file_path, sr=sample_rate, mono=True)
            
            # Trim silence
            y, _ = librosa.effects.trim(y, top_db=30)
            
            # Save
            filename = os.path.basename(file_path)
            new_filename = os.path.splitext(filename)[0] + ".wav"
            output_path = os.path.join(output_dir, new_filename)
            
            sf.write(output_path, y, sample_rate)
            processed_files.append((output_path, os.path.splitext(filename)[0]))
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    return processed_files

def generate_metadata(processed_files, transcript_map, output_csv):
    """
    Generate metadata.csv required for F5-TTS.
    Format: audio_path|text
    """
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        
        for file_path, file_id in processed_files:
            if file_id in transcript_map:
                text = transcript_map[file_id]
                writer.writerow([file_path, text])
            else:
                # Warning: No transcript found
                pass

def main():
    parser = argparse.ArgumentParser(description="Preprocess dataset for F5-TTS")
    parser.add_argument("--input_dir", required=True, help="Raw dataset directory")
    parser.add_argument("--output_dir", required=True, help="Processed dataset directory")
    parser.add_argument("--metadata", help="Path to original metadata/transcript file")
    
    args = parser.parse_args()
    
    # 1. Process Audio
    processed = preprocess_audio(args.input_dir, args.output_dir)
    
    # 2. Process Transcripts (Placeholder logic - needs adaptation per dataset)
    # For OpenSLR/AI4Bharat, we'd parse their specific format here.
    # This is a generic 'file_id: text' map for now.
    transcript_map = {}
    if args.metadata and os.path.exists(args.metadata):
        with open(args.metadata, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|') # Assume pipe separated
                if len(parts) >= 2:
                    transcript_map[parts[0]] = parts[1]
                    
    # 3. Write Final CSV
    csv_path = os.path.join(args.output_dir, "metadata.csv")
    generate_metadata(processed, transcript_map, csv_path)
    print(f"✅ Preprocessing done. Metadata saved to {csv_path}")

if __name__ == "__main__":
    main()
