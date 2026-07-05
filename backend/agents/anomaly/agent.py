from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
#from backend.agents.anomaly.tools import detect_invoice_anomalies 
from dotenv import load_dotenv 

load_dotenv()

anomaly_agent = LlmAgent(
    
    name = "AnomalyAgent",
    
    model = LiteLlm( model="openrouter/openai/gpt-oss-20b:free" ),
    
    description = "Detect anomalies in structured invoices.",
    
    instruction = 
    """
    You are responsible only for anomaly detection.

    Always use the anomaly detection tool.

    Never call the same tool twice if it has already returned successfully.

    Never guess anomalies.

    Never invent findings.

    Return only the findings produced by the tool.
    """

)