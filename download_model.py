import os
# استفاده از میرور عالی که خودت پیدا کردی
os.environ["HF_ENDPOINT"] = "https://hf.devneeds.ir"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1" 
os.environ["HF_HUB_ETAG_TIMEOUT"]="300"
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"]="120"

from langchain_huggingface import HuggingFaceEmbeddings

print("Downloading model from Iranian Mirror... (Please be patient)")
try:
    HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
except Exception as e:
    print(f"\n❌error : {e}")