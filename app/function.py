# standard library modules
import os

# third-party modules
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.prompts import PromptTemplate
import pinecone

# local modules
from constants import (
    INDEX_NAME,
    MODEL_NAME,
    OPENAI_API_KEY,
    #PINECONE_API_ENV,
    #PINECONE_API_KEY,
    KENDRA_INDEX_ID,
    TEMPERATURE
)

'''
def build_chain():
  region = os.environ["AWS_REGION"]
  kendra_index_id = os.environ["KENDRA_INDEX_ID"]

  llm = OpenAI(batch_size=5, temperature=0, max_tokens=300)

  retriever = AmazonKendraRetriever(index_id=kendra_index_id)

  prompt_template = """
  The following is a friendly conversation between a human and an AI. 
  The AI is talkative and provides lots of specific details from its context.
  If the AI does not know the answer to a question, it truthfully says it 
  does not know.
  {context}
  Instruction: Based on the above documents, provide a detailed answer for, {question} Answer "don't know" 
  if not present in the document. 
  Solution:"""
  PROMPT = PromptTemplate(
      template=prompt_template, input_variables=["context", "question"]
  )
  chain_type_kwargs = {"prompt": PROMPT}
    
  return RetrievalQA.from_chain_type(
      llm, 
      chain_type="stuff", 
      retriever=retriever, 
      chain_type_kwargs=chain_type_kwargs, 
      return_source_documents=True
  )

def run_chain(chain, prompt: str, history=[]):
    result = chain(prompt)
    # To make it compatible with chat samples
    return {
        "answer": result['result'],
        "source_documents": result['source_documents']
    }

if __name__ == "__main__":
    chain = build_chain()
    result = run_chain(chain, "What's SageMaker?")
    print(result['answer'])
    if 'source_documents' in result:
        print('Sources:')
        for d in result['source_documents']:
          print(d.metadata['source'])


pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)

'''

def start_conversation():
    """
        Embeddings
    """

    # texts = text_splitter.split_text(saved_file)
    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY
    )
    '''
    vectors = Pinecone.from_existing_index(
        INDEX_NAME,
        embeddings
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            temperature=TEMPERATURE,
            model_name=MODEL_NAME,
            openai_api_key=OPENAI_API_KEY
        ), retriever=vectors.as_retriever())
    '''

    retriever = AmazonKendraRetriever(index_id=KENDRA_INDEX_ID)

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            temperature=TEMPERATURE,
            model_name=MODEL_NAME,
            openai_api_key=OPENAI_API_KEY
        ), retriever=retriever,
        return_source_documents=True)
    return chain


def conversational_chat(chain, query):

    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result['answer'] + '\n \n Source: ' +((result['source_documents'][0]).metadata)['source']
