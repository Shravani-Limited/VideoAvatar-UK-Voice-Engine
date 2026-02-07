import os
import time
import glob
import subprocess

CHECKPOINT_ROOT_INDIA = "/home/ubuntu/regional_voice_engine/f5_tts_repo/src/f5_tts/train/ckpts/india_regional"
CHECKPOINT_ROOT_UK = "/home/ubuntu/regional_voice_engine/f5_tts_repo/src/f5_tts/train/ckpts/uk_regional"
LOG_INDIA = "/home/ubuntu/regional_voice_engine/train_india_split.log"
LOG_UK = "/home/ubuntu/regional_voice_engine/train_uk.log"
STATUS_FILE = "/home/ubuntu/regional_voice_engine/training_status.txt"

def get_latest_dir(root):
    dirs = glob.glob(os.path.join(root, "*/*"))
    if not dirs: return None
    return max(dirs, key=os.path.getmtime)

def get_last_line(path):
    if not os.path.exists(path): return "Waiting for logs..."
    result = subprocess.run(["tail", "-n", "1", path], capture_output=True, text=True)
    return result.stdout.strip()

def monitor():
    print(f"👀 Dual-Monitor Active...")
    while True:
        try:
            india_status = get_last_line(LOG_INDIA)
            uk_status = get_last_line(LOG_UK)
            
            with open(STATUS_FILE, "w") as f:
                f.write("=== REGIONAL VOICE ENGINE STATUS ===\n")
                f.write(f"TIME: {time.ctime()}\n\n")
                f.write("🇮🇳 INDIA (GPUs 0,1):\n")
                f.write(f"Status: {india_status}\n\n")
                f.write("🇬🇧 UK (GPUs 2,3):\n")
                f.write(f"Status: {uk_status}\n")
                f.write("=======================================\n")
                
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(30)

if __name__ == "__main__":
    monitor()
