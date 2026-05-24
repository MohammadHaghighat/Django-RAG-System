import os
from huggingface_hub import snapshot_download

# استفاده از میرور ایرانی برای دور زدن تحریم‌ها و سرعت بالاتر
os.environ["HF_ENDPOINT"] = "https://hf.devneeds.ir"

print("Downloading the embedding model for offline usage...")
print("This may take a few minutes depending on your internet connection.")

try:
    snapshot_download(
        repo_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        local_dir="./local_model_files",
        allow_patterns=["*.safetensors", "*.json", "*.txt", "*.md"]
    )
    print("\n✅ Download complete! The system will now automatically use the local model.")
except Exception as e:
    print(f"\n❌ Error downloading the model: {e}")