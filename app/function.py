# standard library modules
import os

# third-party modules
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import AmazonKendraRetriever
from langchain.prompts import PromptTemplate


# local modules
from constants import (
    MODEL_NAME,
    OPENAI_API_KEY,
    KENDRA_INDEX_ID,
    TEMPERATURE
)

# Build prompt
condense_template= """Given the following conversation and a follow up question, 
rephrase the follow up question to be a standalone question. 

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:

"""
CONDENSE_PROMPT = PromptTemplate(input_variables=["chat_history", "question"], template=condense_template)

qa_template = """You are a chatbot meant to answer queries sent by migrant workers, 
solely with the following context provided. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible. 
If question is in Mandarin, translate it to English before searching the context, then translate the answer back to Mandarin.
Always say "thanks for asking!" at the end of the answer.
{context}

Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=qa_template,)

def start_conversation():

    retriever = AmazonKendraRetriever(index_id=KENDRA_INDEX_ID)
    llm=ChatOpenAI(
            temperature=TEMPERATURE,
            model_name=MODEL_NAME,
            openai_api_key=OPENAI_API_KEY,
            verbose=True
        )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_prompt=CONDENSE_PROMPT,
        retriever=retriever,
        combine_docs_chain_kwargs={'prompt': QA_CHAIN_PROMPT},
        verbose=True,
        return_source_documents=True)

    return chain


def conversational_chat(chain, query):

    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    output = result['answer']
    if 'source_documents' in result:
        output = output + '\n \n Sources:'
        for d in result['source_documents']:
            output += '\n' + d.metadata['source']
    #output = result['answer'] + '\n \n Source: ' + ((result['source_documents'][0]).metadata)['source']
    return output
