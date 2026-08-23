from pathlib import Path
from os import getenv
from langchain_pdf_inspector import PdfInspectorLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_cohere.embeddings import CohereEmbeddings
from dotenv import load_dotenv

load_dotenv(override=True) # with override=True, even if you change .env values, the cached value that was used before won't get in your way when running your code, it will always fetch from the .env file.
EMBEDDING_MODEL = getenv("EMBEDDING_MODEL")
COHERE_API_KEY = str(getenv("COHERE_API_KEY"))
PATH_FOLDER = Path.cwd() / "sample-content"
PDF_SEPARATOR = """


|-------------------|


"""

def database():
    for pdfs in PATH_FOLDER.glob("*.pdf"):
        documents = load_content(pdfs)
        chunks = chunking(documents)
        vectorize_chunks(chunks)

def load_content(pdf_docs: Path):
    """ Função que lê um pdf e retorna o seu conteúdo."""

    fp = str(pdf_docs)

    loader = PdfInspectorLoader(
        file_path=fp
    )

    print(f"Leitura concluída para o arquivo: {pdf_docs.name}")
    return loader.load()

def chunking(docs):
    docs_separator = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=350,
        length_function=len,
        add_start_index=True
    )
    chunks = docs_separator.split_documents(docs)
    print(f"Quantidade de chunks: {len(chunks)}")
    return chunks

def vectorize_chunks(chunks):
    db = Chroma.from_documents(
        chunks,
        CohereEmbeddings(
            model=EMBEDDING_MODEL
        ), # pyright: ignore
        persist_directory="ChromaDB"
    )

if __name__ == "__main__":
    database()
    print("Banco de dados criado!")