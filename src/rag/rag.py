from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from langchain_chroma.vectorstores import Chroma
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from src.rag.vector_db import database

load_dotenv(override=True)

CHROMA_DB_DIR = str(Path.cwd() / "ChromaDB")
EMBEDDING_MODEL = getenv("EMBEDDING_MODEL")
CHAT_MODEL = getenv("CHAT_MODEL")
PDF_SEPARATOR = """


|-------------------|


"""

system_prompt = """
Você é um assistente de inteligência artifical da Santo Pegasus Soluciones.

Responda as perguntas feitas pelo usuário: {pergunta}

usando apenas as informações a seguir: {conhecimento}.

Caso não encontre nenhuma informação relevante, seja honesto e diga que não sabe responder a pergunta.
"""

def asking_to_rag(user_prompt: str):
    """
    Usa a função de embedding e compara a pergunta do usuário com os resultados resgatados da base de conhecimento, gerando uma pontuação que determina a qualidade da fonte para aquela pergunta específica. Caso o banco de dados vetorial não existir, será chamada a função responsável pela criação.
    
    Argumentos:
    - user_prompt: a pergunta do usuário.
    """
    if not Path(CHROMA_DB_DIR).exists():
        print("Banco de dados vetorial não encontrado!\nInicializando a geração de banco.")
        database()

    db = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=CohereEmbeddings(model=EMBEDDING_MODEL) # pyright: ignore
    )

    results = db.similarity_search_with_relevance_scores(user_prompt, k=3)
    if len(results) < 0 or results[0][1] < 0.65:
        print("O agente não encontrou nenhuma resposta relevante")
        return
    page_contents : list[str] = []
    for result in results:
        page_contents.append(result[0].page_content)

    return PDF_SEPARATOR.join(page_contents)

def asking_to_llm(user_prompt: str, rag_knowledge: str | None):
    """
    Faz uma pergunta (levando em conta os argumentos abaixo) para o modelo de linguagem grande (LLM), e o modelo logo em seguida da uma resposta.

    Argumentos:
    - user_prompt: a pergunta do usuário 
    - rag_knowledge: os documentos encontrados pelo RAG com a pergunta do usuário.
    """
    prompt = ChatPromptTemplate.from_template(system_prompt).invoke({
        "pergunta": user_prompt,
        "conhecimento": rag_knowledge
    })

    llm_answer = ChatCohere(
        model=CHAT_MODEL
    ).invoke(prompt)
    print(f"Resposta do Assistente:\n {llm_answer.content}")
    print(f"Métricas de uso:\n {llm_answer.usage_metadata}")