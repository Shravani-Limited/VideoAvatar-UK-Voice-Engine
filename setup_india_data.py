import os

# AI4Bharat IndicTTS consists of multiple languages.
# Hosting is typically on Google Drive or their own servers.
# Best approach: Provide direct wget links if available, or instructions.
# For MIT licensed data, we can try to pull samples if a direct public URL exists.

# According to AI4Bharat GitHub, data is often hosted on Azure/Google Drive.
# We will use a placeholder structure here to guide the user.

LANGUAGES = {
    "hi": "Hindi",
    "ta": "Tamil",
    "mr": "Marathi",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "bn": "Bengali",
    "or": "Odia",
    "as": "Assamese",
    "mni": "Manipuri"
}

def main():
    print("🇮🇳 AI4Bharat IndicTTS Data Setup")
    print("--------------------------------")
    print("Commercial License: MIT (Safe for business use)")
    print("\nSelect languages to setup:")
    
    for code, name in LANGUAGES.items():
        print(f"[{code}] {name}")
        
    print("\n⚠️  NOTE: AI4Bharat datasets are hosted externally.")
    print("To download high-quality single speaker data:")
    print("1. Visit: https://github.com/AI4Bharat/Indic-TTS")
    print("2. Navigate to 'Resources' -> 'Datasets'")
    print("3. Download the 'Mono' (Single Speaker) zip for your target language.")
    print("4. Place the unzipped folder in: regional_voice_engine/datasets/india/<lang_code>/")
    
    # Create directory structure
    base_dir = "datasets/india"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    for code in LANGUAGES.keys():
        lang_dir = os.path.join(base_dir, code)
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
            
    print(f"\n✅ Directory structure created at: {os.path.abspath(base_dir)}")
    print("Please manually download the datasets due to hosting restrictions.")

if __name__ == "__main__":
    main()
