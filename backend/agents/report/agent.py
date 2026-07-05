from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from backend.agents.report.tools import create_audit_report
from dotenv import load_dotenv 

load_dotenv()

report_agent = LlmAgent(

    name="ReportAgent",

    model = LiteLlm(model="groq/llama-3.3-70b-versatile"),

    instruction="""
    You are the Report Generation Agent.

    Your only responsibility is to generate the final audit report.

    Always call the `create_audit_report` tool exactly once.

    The tool already has everything it needs from the workflow state.

    Do not generate the report yourself.
    Do not summarize the report.
    Do not modify the report.
    Do not ask for additional information.
    Do not call any other tool.

    After the tool returns successfully, return the tool output exactly as received.
    """,

    tools=[create_audit_report]
)