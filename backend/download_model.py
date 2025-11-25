# backend/download_model.py
import os
import sys
from huggingface_hub import snapshot_download

def download_model():
    """Download model từ HuggingFace"""
    
    print("=" * 60)
    print("📥 Downloading CosyVoice2 Fine-tuned Model")
    print("=" * 60)
    
    repo_id = "o6Dool/cosyvoice2_finetune_80epoch"
    local_dir = "./models/CosyVoice2-0.5B"
    
    print(f"\n📦 Repository: {repo_id}")
    print(f"📁 Local directory: {local_dir}")
    
    try:
        # Download model
        model_path = snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True,  # Resume nếu bị gián đoạn
        )
        
        print(f"\n✅ Model downloaded successfully!")
        print(f"📍 Location: {os.path.abspath(model_path)}")
        
        # Verify files
        print("\n📋 Verifying downloaded files:")
        required_files = [
            "config.yaml",
            "llm.pt", 
            "flow.pt",
            "hift.pt",
            "speech_tokenizer_v1.onnx"
        ]
        
        all_exist = True
        for file in required_files:
            file_path = os.path.join(model_path, file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path) / (1024**2)  # MB
                print(f"  ✓ {file:30s} {size:>10.2f} MB")
            else:
                print(f"  ✗ {file:30s} MISSING!")
                all_exist = False
        
        if all_exist:
            print("\n✨ All required files are present!")
            return model_path
        else:
            print("\n⚠️  Some files are missing. Please check the download.")
            return None
            
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_model()