from pathlib import Path
from os import getenv
from langchain_pdf_inspector import PdfInspectorLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")
EMBEDDING_MODEL = str(getenv("EMBEDDING_MODEL"))
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
    """ Função que lê um pdf e escreve o seu conteúdo em um arquivo Markdown"""

    with open("pdfs-contents.md", "w") as f:
        f.write("")

    fp : str = str(pdf_docs)

    loader = PdfInspectorLoader(
        file_path=fp
    )

    return loader.load()

def chunking(docs):
    docs_separator = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )
    chunks = docs_separator.split_documents(docs)
    print(len(chunks))
    return chunks

def vectorize_chunks(chunks):
    db = Chroma.from_documents(
        chunks,
        GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL
        ),
        persist_directory="ChromaDB"
    )
    print("Banco de dados criado!")

database()