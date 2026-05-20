import os
# استفاده از میرور عالی که خودت پیدا کردی
os.environ["HF_ENDPOINT"] = "https://hf.devneeds.ir"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1" 
os.environ["HF_HUB_ETAG_TIMEOUT"]="300"
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"]="120"

from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import snapshot_download

print("Downloading model from Iranian Mirror... (Please be patient)")
try:
    path = snapshot_download(
        repo_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        # این خط باعث میشه فقط فایل‌های ضروری مدل دانلود بشن (حدود 470 مگ)
        allow_patterns=["*.safetensors", "*.json", "*.txt", "*.md"]
    )
except Exception as e:
    print(f"\n❌error : {e}")