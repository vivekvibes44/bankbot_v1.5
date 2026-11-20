from rag.chain import answer_question


def test_rag_chain():

    question = "What is the daily ATM withdrawal limit for Ready Bank?"

    print("\nQuestion:", question)
    print("\nGenerating answer...")

    result = answer_question(question)

    print("\n========== RAG RESPONSE ==========")

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(Category: {source['category']})"
        )

    print("\n==================================")


if __name__ == "__main__":
    test_rag_chain()
