import os
from django.conf import settings

# تنظیمات آفلاین و میرور باید اولین چیز باشن
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_ENDPOINT"] = "https://hf.devneeds.ir" 
os.environ["http_proxy"] = "http://127.0.0.1:10808" 
os.environ["https_proxy"] = "http://127.0.0.1:10808"
# ========== همه ایمپورت‌ها در اینجا ==========
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate # این ایمپورت جا افتاده بود
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# ========== تعریف متغیرهای گلوبال ==========
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
CHROMA_PERSIST_DIR = os.path.join(settings.BASE_DIR, "chroma_db")

# ========== تعریف توابع ==========
def process_and_store_document(file_path):
    loader = Docx2txtLoader(file_path)
    docs = loader.load()
    full_text = "\n".join([doc.page_content for doc in docs])
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )
    return full_text

def get_answer_from_ai(question):
    llm = ChatOpenAI(
        model="openai/gpt-oss-120b:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question based only on the following context. 
    If you don't know the answer, just say that you don't know. Don't make up an answer.
    Context: {context}
    Question: {input}
    """)
    
    vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    # این دو خط رو برای دیباگ اضافه کن
    docs = retriever.invoke(question)
    print("\n=== متون پیدا شده توسط دیتابیس ===")
    for doc in docs:
        print(doc.page_content)
    print("==================================\n")
    response = retrieval_chain.invoke({"input": question})
    return response["answer"]