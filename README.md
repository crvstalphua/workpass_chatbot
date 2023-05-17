# Chatbot Application with Streamlit Chat

This is a chatbot application built using Streamlit Chat that utilises several dependencies to provide conversational functionality. 
The application is designed to allow users to interact with a chatbot that can answer questions and provide information by querying a Pinecone vector database.

---

# Requirements
To run the app, you will need to have the following installed:

1. Python 3.6 or higher
2. Virtualenv

---

# Dependencies

1. **langchain**: Framework for LLMs.
2. **langdetect**: Python library for detecting the language of a given text.
3. **openai**: Python library for accessing OpenAI's GPT models.
4. **pinecone-client**: Client library for Pinecone, a vector database that allows you to store and search high-dimensional vectors.
5. **python-dotenv**: Python library for loading environment variables from a .env file.
6. **streamlit**: Python library for building interactive web applications.
7. **streamlit_chat**: Streamlit component that provides a chat widget for use in web applications.
8. **tiktoken**: Fast BPE tokeniser for use with OpenAI's models. (Not from TikTok)

---

# Installation
1. Clone the repository
```bash
$ git clone git@sgts.gitlab-dedicated.com:wog/gvt/gds-ace/general/ace-llm/llm-streamlit-chatbot.git
```
2. Create a virtual environment:
```bash
$ python -m venv .venv
$ source .venv/bin/activate
```
3. Install the dependencies:
```bash
(venv)$ pip install -r requirements.txt
```

---

# Environment Variables

| KEY | VALUE |
|---|---|
| INDEX_NAME | string |
| OPENAI_API_KEY | string |
| PINECONE_API_KEY | string |
| PINECONE_API_ENV | string e.g. "us-west4-gcp" |

# Usage

## Pinecone Index
1. Create a `.env` file and add your `PINECONE_API_KEY` and `PINECONE_API_ENV`.
2. Comment out the `create_vectors()` function in `/app/generate_vectors.py` if you wish to create your indexes programmatically.
```bash
(venv)$ python app/generate_vectors.py
```

## Pinecone Embeddings
1. Once your index instance is ready, you can proceed to create your vector embeddings.
2. Comment out the `create_index()` function in `/app/generate_vectors.py`.
3. Add your `INDEX_NAME` in the `.env` file and your `DOCUMENT` in `constants.py`. 
    - Note: Store documents in `/app/static/`.
4. Execute the following command to geneate the embeddings. It could take a couple of minutes for large documents.
```bash
(venv)$ python app/generate_vectors.py
```

---

# Folder Structure
```bash
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── constants.py
│   ├── function.py
│   ├── generate_vectors.py
│   ├── main.py
│   └── static
└── requirements.txt
```

---

# Local Testing
Execute the following command to test the chatbot locally.
```bash
(venv)$ streamlit run app/main.py
```

---

# Contributing
Contributions are welcome! If you find a bug or want to suggest a new feature, please open an issue or submit a pull request.

---

# License
This project is licensed under the MIT License.
