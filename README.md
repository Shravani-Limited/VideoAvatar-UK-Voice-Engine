# VideoAvatar.ai: UK Regional Voice Engine 🎙️🇬🇧

Master the art of regional British voice cloning with VideoAvatar.ai. This repository contains the core processing, training, and inference scripts for the **VideoAvatar UK Regional Model (v1)**.

## 🚀 Model & Brain
The neural weights for this engine are hosted on Hugging Face due to their large size:
🔗 **[Download Model Weights (Hugging Face)](https://huggingface.co/Shravani-Limited/VideoAvatar-UK-Voice-Engine)**

## 🌟 Key Features
- **Zero-Shot Voice Cloning**: Clone any voice with just 5-10 seconds of source audio.
- **Hyper-Local Accents**: Specialized clusters for Manchester (Northern), London (Southern), Edinburgh (Scottish), Dublin (Irish), and Cardiff (Welsh).
- **Commercial Integrity**: 100% trained on commercially compliant, ethically sourced datasets.
- **Contextual Delivery**: Optimized for Business, Storytelling, Education, and Customer Service tones.

## 🛠️ Included Tools
- **`process_vctk_regional.py`**: High-performance data filtering and metadata generation.
- **`clone_harish_voice.sh`**: One-click script to clone a user voice from an M4A/WAV sample.
- **`generate_diverse_samples.sh`**: Benchmarking suite for multi-accent generation.
- **`run_perfection_suite.sh`**: Advanced fine-tuning and validation pipeline.

## 📦 Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Shravani-Limited/VideoAvatar-UK-Voice-Engine.git
   cd VideoAvatar-UK-Voice-Engine
   ```
2. Install dependencies (Requires Python 3.10+ and CUDA):
   ```bash
   pip install -r requirements.txt
   ```

## ⚖️ License
This project is released under the **Apache 2.0 License**.

Developed with ❤️ by **Shravani Limited**.
