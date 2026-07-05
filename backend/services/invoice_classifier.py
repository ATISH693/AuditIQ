from backend.services.invoice_classifier_llm import ask_llm_invoice_type
from backend.utils.logger import logger

def is_invoice(text: str):

    logger.info("Checking Valid Invoice")
    
    keywords = [
        "invoice",
        "invoice number",
        "invoice no",
        "vendor",
        "bill to",
        "gst",
        "tax invoice",
        "invoice date",
        "amount"
    ]

    text_lower = text.lower()

    score = 0

    for keyword in keywords:
        if keyword in text_lower:
            score += 1

    # High confidence
    if score >= 3:
        return True

    # Low confidence -> ask LLM
    return ask_llm_invoice_type(text)