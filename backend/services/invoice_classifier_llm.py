from dotenv import load_dotenv
from langchain_groq import ChatGroq
from backend.utils.logger import logger
load_dotenv()

llm = ChatGroq(

    model="groq/llama-3.1-8b-instant" ,   
    temperature=0
)

def ask_llm_invoice_type(text: str) -> bool:
    
    logger.info("Check Valid invoice using LLM")

    prompt = f"""
            You are a strict document classifier.

        A document is an invoice ONLY if it contains evidence that it is requesting payment for goods or services.

        Typical invoice fields include:
        - Invoice or Tax Invoice title
        - Invoice Number
        - Seller/Vendor information
        - Buyer/Bill To information
        - Itemized products/services
        - Quantity
        - Unit Price
        - Total Amount

        Return false if the document is:
        - Student information
        - College form
        - Admission letter
        - Receipt
        - Certificate
        - Resume
        - Identity document
        - Application form
        - Bank statement
        - Any document that is not an invoice.

        Return ONLY one word:

        true

        or

        false


    Document:
    {text}
    """

    response = llm.invoke(prompt)

    logger.info("Checked Invoice Using LLM")

    print(response.content)

    return response.content.strip().lower() == "true"