from langchain_core.tools import tool
from rag.chain import answer_question


@tool
def search_banking_knowledge(question: str) -> dict:
    """
    Search the Ready Bank knowledge base for banking policies,
    account information, fees, digital banking information,
    and general banking FAQs.

    Use this tool for questions about Ready Bank products,
    services, policies, requirements, and banking information.
    """

    result = answer_question(question)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }
