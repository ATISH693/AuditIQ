from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from agents.compliance.tools import check_invoice_compliance, save_compliance_result
from dotenv import load_dotenv 

load_dotenv()

compliance_agent = LlmAgent(

    name="ComplianceAgent",

    model = LiteLlm( model="openrouter/openai/gpt-oss-20b:free"  ),

    instruction="""
    You are an invoice compliance auditor.

Workflow:

1. Call check_invoice_compliance exactly ONCE.
2. Wait for the tool response.
3. Decide whether the invoice Passed or Failed.
4. Call save_compliance_result exactly ONCE.
5. Return the result from save_compliance_result.

Rules:
- Never call check_invoice_compliance more than once.
- Never call save_compliance_result more than once.
- After save_compliance_result succeeds, immediately stop.
- Do not repeat the workflow.
- Do not perform any additional reasoning after saving the result.
    """,

    tools=[check_invoice_compliance, save_compliance_result]
)