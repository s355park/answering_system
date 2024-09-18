# from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
import psycopg2
from langchain.schema import BaseRetriever, Document
from retrieve import retrieve_text

class CustomRetriever(BaseRetriever):
    def _get_relevant_documents(self, query):
        # Use your existing function to retrieve a list of strings
        retrieved_strings = retrieve_text(query)
        # print(len(retrieved_strings))
        # Convert the list of strings to a list of dictionaries as expected by LangChain
        documents = [Document(page_content=str(text), metadata={}) for text in retrieved_strings]
        return documents

def get_ans(query):
    retriever = CustomRetriever()

    load_dotenv()

    # Initialize the OpenAI language model
    llm = ChatOpenAI(model_name='gpt-4o', openai_api_key=os.getenv('OPEN_AI_API_KEY2'))  # Ensure your .env file has the correct API key
    

    # Create a RetrievalQA chain with the retriever and language model
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever  # Pass the retriever that retrieves the actual text
    )

    res = qa_chain(query)
    return res['result']