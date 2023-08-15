# standard library modules
import os
import csv  
import pytz
from datetime import datetime

# third-party modules
import boto3
from botocore.config import Config
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

kendra = boto3.client('kendra')


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

    retriever = AmazonKendraRetriever(index_id=KENDRA_INDEX_ID, top_k=3)
    llm=ChatOpenAI(
            temperature=TEMPERATURE,
            model_name=MODEL_NAME,
            openai_api_key=OPENAI_API_KEY,
            verbose=True
        )

    chain = ConversationalRetrievalChain.from_llm(
        combine_docs_chain_kwargs={'prompt': QA_CHAIN_PROMPT},
        llm=llm,
        condense_question_prompt=CONDENSE_PROMPT,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
        verbose = True)

    return chain


def conversational_chat(chain, query):   
    resultIds = []
    queryId = ""

    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    output = result['answer']
    if 'source_documents' in result:
        queryId = result['source_documents'][0].metadata['result_id'][:36] # The queryid is the first 36 characters of the results-id string
        output = output + '\n \n Sources:'
        for d in result['source_documents']:
            output += '\n' + d.metadata['source']
            resultIds.append(d.metadata['result_id'])

    st.session_state['queryid'].append(queryId)   
    st.session_state['resultids'].append(resultIds)            
    #output = result['answer'] + '\n \n Source: ' + ((result['source_documents'][0]).metadata)['source']
    
    # Write to CSVs
    header = ["Time_Enquired", "QueryId", "ResultIds", "Original Question", "Generated Question", "Answer", "Source_Doc", "Chat_History"]
    now = datetime.strftime(datetime.now(pytz.timezone('Asia/Singapore')), "%Y-%m-%d %H:%M:%S")
    data = [now, queryId, resultIds, query, result['generated_question'], result['answer'], result['source_documents'], st.session_state['history']]
    with open("./app/prev_records/qna.csv", 'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(header)
        writer.writerow(data)

    return output

def goodFeedback(queryid, resultids):
    relevance_value = "RELEVANT"
    relevance_items = {}
    tempList = []
    for id in resultids:
        tempList.append(id)
        relevance_items = {
            "ResultId": id,
            "RelevanceValue": relevance_value,
        }

    feedback = kendra.submit_feedback(
        QueryId = queryid,
        IndexId = KENDRA_INDEX_ID,
        RelevanceFeedbackItems = [relevance_items]
    )

    # Write to CSVs
    header = ["Time_Enquired", "QueryId", "ResultIds", "Status", "Feedback"]
    now = datetime.strftime(datetime.now(pytz.timezone('Asia/Singapore')), "%Y-%m-%d %H:%M:%S")
    data = [now, queryid, tempList, "RELEVANT", feedback]
    with open("./app/prev_records/feedback.csv", 'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(header)
        writer.writerow(data)

def badFeedback(queryid, resultids):
    relevance_value = "NOT_RELEVANT"
    relevance_items = {}
    tempList = []
    for id in resultids:
        tempList.append(id)
        relevance_items = {
            "ResultId": id,
            "RelevanceValue": relevance_value,
        }

    feedback = kendra.submit_feedback(
        QueryId = queryid,
        IndexId = KENDRA_INDEX_ID,
        RelevanceFeedbackItems = [relevance_items]
    )

    # Write to CSVs
    header = ["Time_Enquired", "QueryId", "ResultIds", "Status", "Feedback"]
    now = datetime.strftime(datetime.now(pytz.timezone('Asia/Singapore')), "%Y-%m-%d %H:%M:%S")
    data = [now, queryid, tempList, "NOT_RELEVANT", feedback]
    with open("./app/prev_records/feedback.csv", 'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(header)
        writer.writerow(data)