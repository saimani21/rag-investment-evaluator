from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import key_param


dbName = "investment_evaluator"
collectionName = "guidelines"
index = "vector_index"

vectorStore = MongoDBAtlasVectorSearch.from_connection_string(
    key_param.MONGODB_URI,
    dbName + "." + collectionName,
    OpenAIEmbeddings(disallowed_special=(), openai_api_key=key_param.OPENAI_API_KEY),
    index_name=index,
)


def query_data(query):
    retriever = vectorStore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 5,
            "score_threshold": 0.00001
        },
    )

    template = """
    You are a helpful investment analyst.

    Use the following pieces of context to answer the question at the end.

    Rules:
    - If you don't know the answer, say: "Not specified in the guidelines."
    - Only answer if relevant context is present.
    - Keep responses short and accurate.

    Context:
    {context}

    Question:
    {question}
    """

    custom_rag_prompt = PromptTemplate.from_template(template)

    retrieve = {
        "context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])),
        "question": RunnablePassthrough()
    }

    llm = ChatOpenAI(openai_api_key=key_param.OPENAI_API_KEY, temperature=0)

    response_parser = StrOutputParser()

    rag_chain = (
            retrieve
            | custom_rag_prompt
            | llm
            | response_parser
    )

    answer = rag_chain.invoke(query)

    return answer




