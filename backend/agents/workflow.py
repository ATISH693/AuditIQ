from google.adk.agents import SequentialAgent  

from agents.extraction.agent import extraction_agent
from agents.compliance.agent import compliance_agent
from agents.verification.agent import verification_agent
from agents.report.agent import report_agent



audit_workflow = SequentialAgent(
    
    name="AuditWorkflow",

    sub_agents=[
        extraction_agent,
        compliance_agent,
        verification_agent,
        report_agent
    ]

)