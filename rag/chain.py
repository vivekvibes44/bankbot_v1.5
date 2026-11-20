from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from config import GROQ_API_KEY, LLM_MODEL
from rag.retriever import get_retriever




def get_llm():
    """Initialize and return the Groq chat model."""

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing.")

    if not LLM_MODEL:
        raise ValueError("LLM_MODEL is missing.")

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0,
        base_url="https://api.groq.com"
    )



def format_documents(documents):
    """Combine retrieved document chunks into context."""

    formatted_documents = []

    for document in documents:
        source = document.metadata.get("source", "Unknown source")
        category = document.metadata.get("category", "Unknown category")

        formatted_documents.append(
            f"Source: {source}\n"
            f"Category: {category}\n"
            f"Content:\n{document.page_content}"
        )

    return "\n\n".join(formatted_documents)


def answer_question(question: str):
    """
    Retrieve relevant documents and generate a grounded answer.

    Returns the answer and the source documents.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    retriever = get_retriever(search_kwargs={"k": 3})
    documents = retriever.invoke(question)

    if not documents:
        return {
            "answer": "I could not find relevant information in the Ready Bank knowledge base.",
            "source_documents": [],
            "sources": []
        }

    context = format_documents(documents)

    prompt = ChatPromptTemplate.from_template(
        """
        You are the Ready Bank Knowledge Assistant.

        Answer the user's question using ONLY the provided context.

        Rules:
        1. Do not use outside knowledge.
        2. Do not invent banking policies, fees, rates, or requirements.
        3. If the context does not contain the answer, clearly say
           that the information is not available in the knowledge base.
        4. Keep the answer clear and concise.
        5. Remember that Ready Bank is a fictional bank used for
           educational purposes.

        Context:
        {context}

        User question:
        {question}

        Answer:
        """
    )

    llm = get_llm()

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)

    sources = [
        {
            "source": document.metadata.get("source", "Unknown source"),
            "category": document.metadata.get("category", "Unknown category")
        }
        for document in documents
    ]

    return {
        "answer": response.content,
        "source_documents": documents,
        "sources": sources
    }
