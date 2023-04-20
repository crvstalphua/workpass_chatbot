# standard library modules
from pathlib import Path
import os

# third-party modules
from dotenv import find_dotenv, load_dotenv
from langchain.document_loaders import CSVLoader, UnstructuredPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone

# local modules


load_dotenv(find_dotenv())

INDEX_NAME = os.getenv('INDEX_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')


embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
namespace = "migrant_domestic_workers"

abs_path = Path().absolute()
pdf_path = f'{abs_path}/app/static/mdw-handy-guide-english-bahasa-indonesia.pdf'


def create_vectors(
    embeddings,
    index_name,
    namespace,
    pdf_path
):
    """
        Embeddings
    """
    
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )

    loader = UnstructuredPDFLoader(pdf_path)
    data = loader.load()

    print(f'You have {len(data)} document(s) in your data')
    print(f'There are {len(data[0].page_content)} characters in your document')

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    texts = text_splitter.split_documents(data)

    print(f'Now you have {len(texts)} documents')

    # docsearch = Pinecone.from_existing_index(index_name, embeddings)
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

    query = "How do I care for family members?"
    docs = docsearch.similarity_search(query, include_metadata=True)

    print(docs)


if __name__ == "__main__":
    create_vectors(embeddings, INDEX_NAME, namespace, pdf_path)
