import os 
from dotenv import load_dotenv 
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import JsonOutputParser 
from langchain_groq import ChatGroq

load_dotenv()

prompt = PromptTemplate(
    template = """ 
    Extract invoice details from the text below.

    Return ONLY valid JSON with keys:
    - invoice_number
    - vendor
    - amount
    - date
    - gst

    If a field is missing, set it as null.

    Text:
    {text}
    """,
    input_variables = ["text"] 
)

model = ChatGroq(
    model = "llama-3.1-8b-instant", 
    api_key = os.getenv("GROQ_API_KEY"),
    temperature = 0
    )

parser = JsonOutputParser()

chain = prompt | model | parser 

def ask_llm(text: str) : 
    return chain.invoke({"text" : text}) 




