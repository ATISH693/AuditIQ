from google.adk.tools import ToolContext
from backend.services.invoice_parser import extract_data
from backend.database import save_invoice
from backend.utils.logger import logger


def extract_invoice_information(tool_context: ToolContext):

    """
    Extract invoice information from PDF text.
    """

    logger.info("Extraction Agent started.")

    pdf_text = tool_context.state["pdf_text"]

    invoice = extract_data(pdf_text)

    tool_context.state["invoice"] = invoice["data"]

    save_invoice(invoice["data"])

    logger.info("Invoice information extracted successfully.")

    return invoice