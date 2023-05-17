# standard library modules
from pathlib import Path
import os

# third-party modules
from dotenv import find_dotenv, load_dotenv
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone

# local modules
from constants import (
    DOCUMENT,
    INDEX_NAME,
    OPENAI_API_KEY,
    PINECONE_API_ENV,
    PINECONE_API_KEY
)


embeddings = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY
)
namespace = "migrant_domestic_workers"

abs_path = Path().absolute()
pdf_path = f'{abs_path}/app/static/{DOCUMENT}'


def create_index():
    pinecone.create_index(
        INDEX_NAME,
        dimension=1536,
        metric='cosine',
        pods=1,
        replicas=1,
        pod_type='p2.x1'
    )


def create_vectors(
    embeddings,
    index_name,
    namespace,
    pdf_path
):
    """
        Embeddings
    """

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

    docsearch = Pinecone.from_texts(
        [t.page_content for t in texts],
        embeddings,
        index_name=index_name
    )

    # query = "This is my first time in Singapore"
    # docs = docsearch.similarity_search(
    #     query,
    #     include_metadata=True
    # )

    # print(docs)


if __name__ == "__main__":
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    # create_index()
    create_vectors(
        embeddings,
        INDEX_NAME,
        namespace,
        pdf_path
    )
