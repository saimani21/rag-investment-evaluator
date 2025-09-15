import unicodedata
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
import key_param

db_name = "investment_evaluator"
collection_name = "guidelines"
index_name = "vector_index"

vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    key_param.MONGODB_URI,
    f"{db_name}.{collection_name}",
    OpenAIEmbeddings(disallowed_special=(), openai_api_key=key_param.OPENAI_API_KEY),
    index_name=index_name,
)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3, "score_threshold": 0.01})

memo_eval_prompt = PromptTemplate.from_template("""
You are an investment analyst. Given the internal investment guidelines (context) and a list of extracted fields from a startup's investment memo, evaluate whether each field complies with the firm's criteria.

IMPORTANT: 
- Do NOT use Markdown (like *italic*, **bold**, etc).
- Do NOT include formatted Unicode (like 𝑀𝑅𝑅).
- Output must be plain text ONLY.

Instructions:
- For each field, mention the actual value given in the memo.
- Compare that value to the relevant policy in the context.
- for fields like startup name ,foundername (which are not used for evaluation just give field name and value)
- Clearly explain whether the value complies, violates, or is missing required justification.
- If the guideline doesn't mention that field, return: "No relevant guideline found."
- Keep each explanation short and precise — 1–2 sentences per field.
- Dont miss any field 

Context:
{context}

Startup Memo Fields:
{fields}

Return your evaluation as a JSON object in this format:
{{
  "Funding Requested": "Funding requested is $1,200,000. This exceeds $1M, so board approval is required.",
  "Sector": "Sector is Healthcare AI, which aligns with preferred sectors like HealthTech.",
  ...
}}

 
""")


llm = ChatOpenAI(openai_api_key=key_param.OPENAI_API_KEY, temperature=0)
parser = StrOutputParser()



def evaluate_memo_fields(fields_dict: dict) -> dict:
    context_chunks = []
    for field, value in fields_dict.items():
        query = f"{field}: {value}"
        docs = retriever.get_relevant_documents(query)
        print(f"\n=== Retrieved Contexts for: {field} ===")
        for i, doc in enumerate(docs, 1):
            print(f"[{i}] {doc.page_content}\n")

        context_chunks.extend(docs)


    unique_contexts = list({doc.page_content for doc in context_chunks})
    combined_context = "\n\n".join(unique_contexts)
    print("\n=== Combined Context Passed to LLM ===")
    for i, context in enumerate(unique_contexts, 1):
        print(f"[{i}] {context}\n")

    field_str = "\n".join([f"{k}: {v}" for k, v in fields_dict.items()])

    prompt_input = memo_eval_prompt.format(context=combined_context, fields=field_str)

    raw_result = llm.invoke(prompt_input)
    try:
        eval_result = parser.invoke(raw_result)
        return eval(eval_result) if isinstance(eval_result, str) else eval_result
    except:
        return {"error": "Failed to parse LLM result.", "raw": raw_result}

