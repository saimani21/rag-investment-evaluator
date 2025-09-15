<<<<<<< HEAD
# rag-investment-evaluator
=======
<<<<<<< HEAD
# rag-investment-evaluator
=======
# 💼 RAG Investment Evaluator

**RAG Investment Evaluator** is an AI-powered Streamlit app that automates the evaluation of startup investment memos using internal venture capital (VC) guidelines.

It uses **Retrieval-Augmented Generation (RAG)** by combining:
- MongoDB Atlas Vector Search for guideline retrieval,
- ChromaDB for memo storage,
- LangChain for orchestration,
- OpenAI GPT for intelligent evaluation.

---

## 🚀 Features

- 📥 Upload startup investment memos as PDFs  
- ✂️ Auto-summarize and store memos in ChromaDB  
- 📚 Retrieve relevant VC guidelines from MongoDB  
- 🧠 Evaluate memo fields using GPT (e.g., Funding, MRR, Team Info)  
- 🧾 Generate a structured PDF report  
- 💬 Interactive chatbot to query internal policies  

---

## 🧠 System Architecture

```plaintext
                         ┌────────────────────┐
                         │  Guidelines PDF    │
                         └────────┬───────────┘
                                  ↓
                    ┌────────────────────────────┐
                    │  Chunk + Embed + Store     │
                    │  (MongoDB Atlas V.S.)      │
                    └────────┬───────────────────┘
                             ↓
User Uploads Memo   ┌────────────────────────────┐
      PDF  ────────▶│ Summarize + Store in Chroma│
                   └────────┬────────────────────┘
                            ↓
         ┌────────────────────────────────────┐
         │ Evaluate Each Memo Field           │
         │ - Retrieve matching guidelines     │
         │ - Evaluate compliance using GPT    │
         └────────────────────────────────────┘
                            ↓
              ┌────────────────────────────┐
              │ Generate Evaluation Report │
              │      (Downloadable PDF)    │
              └────────────────────────────┘

+ Interactive Chatbot (MongoDB vector search + GPT)
```
---

## 💡 How It Works – High-Level Overview

🔹 **VC Guidelines Ingested and Embedded**  
Internal venture capital guidelines are processed, chunked into meaningful sections, and embedded using vector representations. These embeddings are stored in **MongoDB Atlas Vector Search** to enable semantic retrieval.

🔹 **Memo PDFs Uploaded and Analyzed**  
Users can upload startup investment memos in PDF format. Each memo is automatically summarized, relevant fields (e.g., funding requested, MRR, sector) are extracted, and the content is stored in **ChromaDB** for local semantic indexing.

🔹 **Field-by-Field Evaluation Using GPT**  
For each extracted memo field, the system retrieves the most relevant policy segments from MongoDB Atlas. These are passed along with the memo values to **OpenAI GPT**, which performs a contextual evaluation — determining whether the memo complies with the firm’s investment criteria.

🔹 **Automated PDF Report Generation**  
The results of the evaluation are compiled into a professionally formatted **PDF report**, showing the actual field values, matched policy segments, and compliance explanations.

🔹 **Interactive Policy Chatbot**  
The application includes a chatbot interface that allows users to ask **guideline-related questions** (e.g., “What requires board approval?”). It uses **vector-based retrieval** from MongoDB to fetch the most relevant context and respond intelligently via GPT.


---

## 📂 Project Structure

```bash
.
├── app.py                     # Streamlit main app
├── utils/
│   ├── chat_handler.py        # Chatbot logic for answering guideline-related queries
│   ├── evaluate_fields.py     # Field-level evaluator using GPT and retrieved guidelines
│   ├── load_guidelines.py     # Loads and chunks guidelines PDF into MongoDB Atlas Vector Search
│   ├── summarize_memo.py      # Summarizes uploaded memo and stores content in ChromaDB
│   ├── report_utils.py        # PDF report generation logic
├── key_param.py               # API keys (MongoDB URI, OpenAI Key)
├── requirements.txt           # Required Python packages
├── chroma_db/
│   └── memo_chunks/           # ChromaDB local vector DB storage (SQLite format)
├── data/                      # Uploaded guideline and memo PDFs
│   └── .DS_Store              # MacOS file (can be ignored/deleted)
├── README.md                  # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/rag-investment-evaluator.git
cd rag-investment-evaluator
```

### 2️⃣ Install Dependencies

Make sure Python 3.9+ is installed.

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Your API Keys

Create a `key_param.py` file:

```python
# key_param.py
MONGODB_URI = "your_mongodb_atlas_connection_string"
OPENAI_API_KEY = "your_openai_api_key"
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The app will open in your browser.

---

## 🧪 How It Works

### 📝 Step 1: Load Guidelines (Run Once)
Before running the load_guidelines.py script:
  - Place your guideline or policy PDF in the data/ folder.
  - Update the file path inside load_guidelines.py to match the PDF name.
```bash
python load_guidelines.py
```

This loads and vectorizes internal VC guidelines into MongoDB Atlas.

---

### 📄 Step 2: Upload Memo PDF via App

- Upload your startup investment memo through the UI.
- The app will:
  - 🔍 Summarize the content  
  - 🧠 Extract key fields (Funding, Sector, MRR, etc.)  
  - 💾 Store content and metadata in ChromaDB  

---

### ✅ Step 3: Evaluate Memo Fields

- For each extracted field:
  - Retrieve relevant guidelines from MongoDB
  - Use GPT to evaluate compliance
- Download the final PDF evaluation report

---

### 💬 Step 4: Ask Policy Questions via Chatbot

- Ask anything like:
  - “What’s the funding limit?”
  - “What sectors are restricted?”
  - “What requires board approval?”
- The chatbot uses MongoDB Atlas Vector Search + GPT to respond

---

## 📌 Dependencies

```txt
streamlit
langchain
langchain-community
langchain-openai
pymongo
PyMuPDF
fpdf
```

---



## 📬 Contact

Built by [Akhileswari Pemmanaboina](mailto:akhileswari712@gmail.com)

Feel free to fork, improve, and contribute!

> Empowering investors with AI-driven memo evaluation 🧠
>>>>>>> a2e9374 (Initial commit of the rag evaluator project)
>>>>>>> d6076a5 (Initial commit of the Rag project)
