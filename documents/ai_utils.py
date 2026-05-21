import os
from django.conf import settings

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_ENDPOINT"] = "https://hf.devneeds.ir" 

# این دو خط رو حتماً اضافه کن (پورت رو بر اساس فیلترشکن خودت تنظیم کن: مثلاً 10808 یا 7890)
os.environ["http_proxy"] = "http://127.0.0.1:10808" 
os.environ["https_proxy"] = "http://127.0.0.1:10808"

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
CHROMA_PERSIST_DIR = os.path.join(settings.BASE_DIR, "chroma_db")

# تغییر 1: اضافه شدن doc_id به ورودی تابع
def process_and_store_document(file_path, doc_id):
    file_extension = file_path.lower().split('.')[-1]
    
    if file_extension == 'docx':
        loader = Docx2txtLoader(file_path)
    elif file_extension == 'pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension == 'txt':
        loader = TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError("فرمت فایل پشتیبانی نمی‌شود!")

    docs = loader.load()
    full_text = "\n".join([doc.page_content for doc in docs])
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    # تغییر 2: چسباندن آیدی سند به تکه متن‌ها (Metadata)
    for chunk in chunks:
        chunk.metadata["doc_id"] = str(doc_id)
    
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PERSIST_DIR)
    return full_text

# تغییر 3: تابع جدید برای حذف از دیتابیس برداری
def delete_document_from_chroma(doc_id):
    vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)
    try:
        # پیدا کردن و حذف بردارهایی که آیدی این سند رو دارن
        vectorstore._collection.delete(where={"doc_id": str(doc_id)})
        print(f"Vectors for doc_id {doc_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting from ChromaDB: {e}")

def get_answer_from_ai(question):
    llm = ChatOpenAI(
        model= "openai/gpt-oss-120b:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    prompt_template = ChatPromptTemplate.from_template("""
    Answer the user's question based only on the following context. 
    If you don't know the answer, just say "اطلاعاتی در این باره در اسناد یافت نشد.".
    
    Context: {context}
    
    Question: {input}
    """)
    
    vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # تغییر اصلی اینجاست!
    response = retrieval_chain.invoke({"input": question})
    
    # استخراج نام اسناد منبع
    source_documents = []
    clean_contexts = [] # برای تمیز کردن متن‌های ارسالی به فرانت‌اند
    
    if "context" in response and response["context"]:
        for doc in response["context"]:
            # تمیز کردن متن (کشیدن بیرون از ساختار LangChain)
            clean_contexts.append(doc.page_content)
            
            if 'doc_id' in doc.metadata:
                source_documents.append(f"سند شماره {doc.metadata['doc_id']}")
    
    unique_sources = list(set(source_documents))

    # چسباندن متن‌های تمیز شده به هم
    formatted_context_for_display = "\n\n---\n\n".join(clean_contexts)
    
    # ساخت پرامپت نهایی فقط برای نمایش زیبا در فرانت‌اند
    display_prompt = prompt_template.format(context=formatted_context_for_display, input=question)

    return {
        "answer": response["answer"],
        "sources": unique_sources,
        "prompt": display_prompt
    }