import os
from huggingface_hub import snapshot_download

# استفاده از میرور ایرانی برای سرعت بالا
os.environ["HF_ENDPOINT"] = "https://hf.devneeds.ir"

print("در حال دانلود مدل به داخل پوشه پروژه (لطفا صبور باشید)...")
snapshot_download(
    repo_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    local_dir="./local_model_files", # 👈 جادو اینجاست! مدل همینجا ذخیره میشه
    allow_patterns=["*.safetensors", "*.json", "*.txt", "*.md"]
)
print("✅ دانلود تمام شد. حالا مدل داخل پوشه local_model_files قرار دارد!")