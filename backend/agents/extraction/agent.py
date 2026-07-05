from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from agents.extraction.tools import extract_invoice_information
from dotenv import load_dotenv 

load_dotenv()

extraction_agent = LlmAgent(
    
    name="ExtractionAgent",

    model = LiteLlm(model="openrouter/openai/gpt-oss-20b:free"),

    instruction="""
        You are responsible for extracting invoice information.

        Always use the extraction tool.

        Never call the same tool twice if it has already returned successfully.

        Do not audit invoices.

        Return structured data only.
        """,

    tools=[extract_invoice_information]
)

