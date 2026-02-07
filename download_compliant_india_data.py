import os
import requests
from bs4 import BeautifulSoup
import subprocess

# Safe OpenSLR IDs for Indian Languages (Commercially usable):
# 64: Marathi (CC-BY-SA 4.0)
# 78: Multilingual Indian (CC-BY-SA 4.0) - Gujarati, Kannada, Marathi, Tamil, Telugu
# 104: Hindi-English code-switched (CC-BY-SA 4.0)
DATASET_IDS = {
    "marathi_cc_by_sa": [64],
    "multilingual_indic_cc_by_sa": [78],
    "hindi_english_cc_by_sa": [104]
}

BASE_URL_TEMPLATE = "https://www.openslr.org/{}/"
OUTPUT_DIR = "datasets/india"

def get_download_links(slr_id):
    url = BASE_URL_TEMPLATE.format(slr_id)
    print(f"🔍 Scanning {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('.tar.gz') or href.endswith('.zip'):
                if not href.startswith('http'):
                    href = f"https://www.openslr.org/{href}"
                links.append(href)
        return links
    except Exception as e:
        print(f"❌ Error fetching links for SLR{slr_id}: {e}")
        return []

def download_file(url, target_folder):
    filename = url.split('/')[-1]
    filepath = os.path.join(target_folder, filename)
    
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 1024 * 1024:
            print(f"✅ File valid: {filename} ({size/1024/1024:.2f} MB)")
            return filepath
        
    print(f"⬇️  Downloading {filename}...")
    try:
        subprocess.run(["wget", "-c", "-P", target_folder, url], check=True)
        return filepath
    except subprocess.CalledProcessError:
        print(f"❌ Failed to download {filename}")
        return None

def main():
    print("🇮🇳 Compliant Indian Regional Voice Downloader")
    print("---------------------------------------------")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for lang, ids in DATASET_IDS.items():
        print(f"\n🌍 Processing {lang} datasets...")
        for slr_id in ids:
            links = get_download_links(slr_id)
            for link in links:
                download_file(link, OUTPUT_DIR)
                
    print("\n✅ Compliant India Data Download complete.")

if __name__ == "__main__":
    main()
