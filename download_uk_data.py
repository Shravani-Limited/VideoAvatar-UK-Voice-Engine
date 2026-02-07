import os
import requests
from bs4 import BeautifulSoup
import subprocess

# OpenSLR ID for "Crowdsourced high-quality UK and Ireland English Dialect"
DATASET_ID = 83
BASE_URL = f"https://www.openslr.org/{DATASET_ID}/"
OUTPUT_DIR = "datasets/uk"

def get_download_links():
    """Scrape OpenSLR page for .tar.gz files"""
    print(f"🔍 Scanning {BASE_URL}...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            print(f"debug link: {href}")
            if href.endswith('.tar.gz') or href.endswith('.zip'):
                # Handle relative links
                if not href.startswith('http'):
                    href = f"https://www.openslr.org/{href}"
                links.append(href)
        return links
    except Exception as e:
        print(f"❌ Error fetching links: {e}")
        return []

def download_file(url, target_folder):
    """Download a file using wget"""
    filename = url.split('/')[-1]
    filepath = os.path.join(target_folder, filename)
    
    if os.path.exists(filepath):
        print(f"✅ File already exists: {filename}")
        return filepath
        
    print(f"⬇️  Downloading {filename}...")
    try:
        subprocess.run(["wget", "-c", "-P", target_folder, url], check=True)
        return filepath
    except subprocess.CalledProcessError:
        print(f"❌ Failed to download {filename}")
        return None

def main():
    print("🇬🇧 UK Regional Dialect Downloader (OpenSLR 83)")
    print("---------------------------------------------")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    links = get_download_links()
    if not links:
        print("⚠️  No files found to download.")
        return

    print(f"Found {len(links)} files.")
    for link in links:
        # For SLR83, files are usually structured. We download all for now
        # and will filter by speaker metadata later.
        download_file(link, OUTPUT_DIR)
        
    print("\n✅ Download complete. Next step: Extract and filter by dialect.")
    print(f"📂 Files saved to: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
