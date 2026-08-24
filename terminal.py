from src.rag.rag import asking_to_llm, asking_to_rag

if __name__ == "__main__":
    userprompt = input("> ")
    knowledge = asking_to_rag(userprompt)

    print(asking_to_llm(
        userprompt,
        knowledge
    ))
