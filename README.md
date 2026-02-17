# VideoAvatar.ai: UK Regional Voice Engine (v2 - 420k) 🎙️🇬🇧

Master the art of regional British voice cloning with VideoAvatar.ai. This repository contains the core configuration and documentation for the **VideoAvatar UK Regional Model (v2)**.

## 🚀 Model & Brain
The neural weights for this engine are hosted on Hugging Face:
🔗 **[Download v2 Model Weights (Hugging Face)](https://huggingface.co/Shravani-Limited/VideoAvatar-UK-Voice-Engine)**

> **Version 2.0 (Step 420,000)** - Released Feb 17, 2026.
> Improved prosody, stability, and vocabulary handling.

## 🚨 CRITICAL USAGE INSTRUCTION
**You MUST set `text_mask_padding=False` in your inference configuration.**
Failure to do so will result in "fast" or "scrambled" speech (chipmunk effect).

Use the included `config_v2.yaml` which has this setting correctly applied.

```bash
# Example Inference Command
python3 infer_cli.py \
    --model_cfg config_v2.yaml \
    --ckpt_file uk_regional_v2_420k.pt \
    ...
```

## 🌟 Key Features
- **Zero-Shot Voice Cloning**: Clone any voice with just 5-10 seconds of source audio.
- **Hyper-Local Accents**: Specialized clusters for Manchester (Northern), London (Southern), Edinburgh (Scottish), Dublin (Irish), and Cardiff (Welsh).
- **Commercial Integrity**: 100% trained on commercially compliant, ethically sourced datasets.
- **Contextual Delivery**: Optimized for Business, Storytelling, Education, and Customer Service tones.

## 🛠️ Included Files
- **`config_v2.yaml`**: The verified configuration file for the v2 model.
- **`samples/`**: Example audio generated with this model.

## 📦 Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Shravani-Limited/VideoAvatar-UK-Voice-Engine.git
   cd VideoAvatar-UK-Voice-Engine
   ```
2. Download the model checkpoint from Hugging Face.
3. Install the F5-TTS dependencies.

## ⚖️ License
This project is released under the **Apache 2.0 License**.

Developed with ❤️ by **Shravani Limited**.
