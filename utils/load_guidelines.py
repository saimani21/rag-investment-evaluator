from pymongo import MongoClient
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import key_param

client = MongoClient(key_param.MONGODB_URI)
db_name = "investment_evaluator"
collection_name = "guidelines"
collection = client[db_name][collection_name]

pdf_path = "sample_guidelines.pdf"  # Replace with your actual path
loader = PyPDFLoader(pdf_path)
pages = loader.load()

cleaned_pages = [page for page in pages if len(page.page_content.split(" ")) > 20]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=150
)
split_docs = text_splitter.split_documents(cleaned_pages)

print(f"🔍 Total Chunks to Embed: {len(split_docs)}")

embedding_model = OpenAIEmbeddings(
    disallowed_special=(),
    openai_api_key=key_param.OPENAI_API_KEY
)



vectorstore = MongoDBAtlasVectorSearch.from_documents(
    documents=split_docs,
    embedding=embedding_model,
    collection=collection,
    index_name="vector_index"  # Must match your created index
)

print("✅ Guideline PDF processed and stored in MongoDB Atlas successfully.")
