import torch
from safetensors.torch import load_file, save_file
import os

def pad_weights(source_path, target_path, new_vocab_size):
    print(f"🔄 Padding {source_path} to vocab size {new_vocab_size}...")
    weights = load_file(source_path)
    
    # 1. Detect EMA vs Normal
    is_ema = any(k.startswith("ema_model.") for k in weights.keys())
    prefix = "ema_model." if is_ema else ""
    
    # Key for text embedding
    # In F5-TTS, it's often 'transformer.text_embed.text_embed.weight'
    # Base key search
    embed_key = None
    for k in weights.keys():
        if "text_embed.text_embed.weight" in k:
            embed_key = k
            break
            
    if not embed_key:
        print("❌ Could not find text embedding key!")
        return

    old_weight = weights[embed_key]
    old_vocab_size, text_dim = old_weight.shape
    print(f"   Old vocab size: {old_vocab_size}, Text dim: {text_dim}")

    if new_vocab_size <= old_vocab_size:
        print("   New vocab size is smaller or equal. No padding needed.")
        # But we still want to rename keys to remove Prefix if it exists, 
        # so the trainer loads it as a normal model if it's not and EMA resume.
        pass
    else:
        # Create new weight tensor
        new_weight = torch.randn((new_vocab_size, text_dim)) * 0.02
        # Copy existing weights
        new_weight[:old_vocab_size, :] = old_weight
        weights[embed_key] = new_weight
        print(f"   ✅ Padded {embed_key} to {new_vocab_size}")

    save_file(weights, target_path)
    print(f"🎉 Saved padded weights to {target_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python pad_weights.py <src> <dst> <vocab_size>")
    else:
        pad_weights(sys.argv[1], sys.argv[2], int(sys.argv[3]))
