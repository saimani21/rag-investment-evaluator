import os
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import key_param

CHROMA_DIR = "./chroma_db/memo_chunks"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def process_memo(pdf_path: str) -> dict:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    cleaned_pages = [p for p in pages if len(p.page_content.split(" ")) > 20]

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(cleaned_pages)

    if not os.path.exists(CHROMA_DIR):
        os.makedirs(CHROMA_DIR)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    vectordb.persist()

    print("✅ Memo chunks stored in ChromaDB.")

    full_text = "\n\n".join([doc.page_content for doc in chunks])

    prompt = PromptTemplate.from_template("""
    You are an AI assistant helping a venture firm extract key fields from an investment memo.

    Memo content:
    {memo}

    Extract and return the following fields:
    - Funding Requested
    - Sector
    - Monthly Revenue / Traction
    - Founder Background
    - Stage (Seed, Series A, etc.)
    - Location
    
    extract if any other fields are present .
    if the data of any field is not there dont extract that field
    Respond as a JSON object.
    """)

    llm = ChatOpenAI(openai_api_key=key_param.OPENAI_API_KEY, temperature=0, model="gpt-4")
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"memo": full_text})

    try:
        fields = json.loads(result)
        print("✅ Fields extracted from memo.")
    except json.JSONDecodeError:
        print("⚠️ Failed to parse JSON from model response.")
        fields = {}
    print(fields)
    return fields


