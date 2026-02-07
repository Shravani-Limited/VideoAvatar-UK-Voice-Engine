from huggingface_hub import HfApi, login
import os
import sys

TOKEN = "your_huggingface_token_here"
REPO_ID = "Shravani-Limited/VideoAvatar-UK-Voice-Engine"

print(f"🔑 Logging in to Hugging Face...")
login(token=TOKEN)

api = HfApi()

# Define files to upload
files_to_upload = {
    "/home/ubuntu/regional_voice_engine/f5_tts_repo/ckpts/uk_regional/uk_regional_v1.pt": "uk_regional_v1.pt",
    "/home/ubuntu/regional_voice_engine/datasets/uk/arrow_data/vocab.txt": "vocab.txt"
}

for local_path, repo_path in files_to_upload.items():
    if os.path.exists(local_path):
        print(f"📤 Uploading {repo_path}...")
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=repo_path,
            repo_id=REPO_ID,
            repo_type="model"
        )
        print(f"✅ {repo_path} uploaded successfully.")
    else:
        print(f"⚠️ File not found: {local_path}")

# Define Model Card content
model_card = """---
license: apache-2.0
language:
- en
tags:
- text-to-speech
- voice-cloning
- f5-tts
- regional-accents
- uk
---

# VideoAvatar.ai: UK Regional Voice Engine (v1)
Developed by **Shravani Limited**, this model is a state-of-the-art Zero-Shot Voice Cloning engine specifically fine-tuned to master the diverse regional accents of the United Kingdom.

## 🌟 Capabilities
- **Zero-Shot Cloning**: Clone any voice perfectly with just 3-10 seconds of reference audio. Master your own identity in seconds.
- **UK Regional Mastery**: Optimized for high-fidelity output in:
  - **Northern**: Manchester, Scouse, Geordie.
  - **Southern**: London (Estuary & MLE).
  - **Celtic**: Scottish (Fife/Edinburgh), Irish (Dublin/Belfast), Welsh (Cardiff).
- **Commercial Ready**: 100% trained on ethically sourced, commercially cleared datasets (CC-BY 4.0).

## 🛠️ Technical Details
- **Architecture**: F5-TTS (Diffusion-based Transformer).
- **Updates**: 174,000 steps on 4x NVIDIA A10G GPUs.
- **Precision**: EMA (Exponential Moving Average) weights for stable, human-quality prosody.

## 🚀 Usage
This model is designed for use with the F5-TTS inference pipeline. 

## ⚖️ License & Ethics
This model is released under the **Apache 2.0** license. Shravani Limited is committed to ethical AI—please ensure you have the rights to any voice you attempt to clone.
"""

print(f"📝 Updating Model Card (README.md)...")
api.upload_file(
    path_or_fileobj=model_card.encode(),
    path_in_repo="README.md",
    repo_id=REPO_ID,
    repo_type="model"
)
print(f"✅ Model Card updated successfully.")

print(f"🎉 All tasks completed! Model is live at https://huggingface.co/{REPO_ID}")
