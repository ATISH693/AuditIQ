from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from backend.agents.verification.tools import verify_audit
from dotenv import load_dotenv 

load_dotenv()

verification_agent = LlmAgent(

    name="VerificationAgent",

    model = LiteLlm( model="openrouter/openai/gpt-oss-20b:free"  ),
    
    instruction="""
    You are a senior audit verifier.

    Always use the verification tool.

    Never call the same tool twice if it has already returned successfully.
    
    Verify the audit results.

    Return only the verified result.
    """,

    tools=[verify_audit]
)