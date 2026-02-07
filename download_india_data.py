import os
import requests
from bs4 import BeautifulSoup
import subprocess

# OpenSLR IDs for Indian Languages:
# 40: Hindi (ASR/TTS useful)
# 64: Marathi
# 65: Tamil (?) - checking typical IDs
# 78: Multilingual Indian (Gujarati, Kannada, Malayalam, Marathi, Tamil, Telugu) - THIS IS THE GOLDMINE
# 113: Hindi
DATASET_IDS = {
    "hindi": [40],
    "marathi": [64],
    "hindi_extra": [113],
    "odia_bengali_mix": [103], # SLR103 contains Odia, Bengali, Hindi (ASR)
    "kashmiri": [122]
}

BASE_URL_TEMPLATE = "https://www.openslr.org/{}/"
OUTPUT_DIR = "regional_voice_engine/datasets/india"

def get_download_links(slr_id):
    """Scrape OpenSLR page for download links"""
    url = BASE_URL_TEMPLATE.format(slr_id)
    print(f"🔍 Scanning {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Filter for typically large archive files
            if href.endswith('.tar.gz') or href.endswith('.zip'):
                if not href.startswith('http'):
                    href = f"https://www.openslr.org/{href}"
                links.append(href)
        return links
    except Exception as e:
        print(f"❌ Error fetching links for SLR{slr_id}: {e}")
        return []

def download_file(url, target_folder):
    """Download a file using wget"""
    filename = url.split('/')[-1]
    filepath = os.path.join(target_folder, filename)
    
    # Check if file exists AND is not empty (e.g. > 1MB)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 1024 * 1024: # 1MB
            print(f"✅ File valid: {filename} ({size/1024/1024:.2f} MB)")
            return filepath
        else:
            print(f"⚠️  File incomplete or empty: {filename}. Deleting...")
            os.remove(filepath)
        
    print(f"⬇️  Downloading {filename}...")
    try:
        # Use wget
        subprocess.run(["wget", "-c", "-P", target_folder, url], check=True)
        return filepath
    except subprocess.CalledProcessError:
        print(f"❌ Failed to download {filename}")
        return None

def main():
    print("🇮🇳 Indian Regional Voice Downloader (OpenSLR)")
    print("---------------------------------------------")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for lang, ids in DATASET_IDS.items():
        print(f"\n🌍 Processing {lang} datasets...")
        for slr_id in ids:
            links = get_download_links(slr_id)
            for link in links:
                download_file(link, OUTPUT_DIR)
                
    print("\n✅ India Data Download complete.")

if __name__ == "__main__":
    main()
