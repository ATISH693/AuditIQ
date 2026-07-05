from google.adk.agents import SequentialAgent  

from backend.agents.extraction.agent import extraction_agent
from backend.agents.anomaly.agent import anomaly_agent
from backend.agents.compliance.agent import compliance_agent
from backend.agents.verification.agent import verification_agent
from backend.agents.report.agent import report_agent



audit_workflow = SequentialAgent(
    
    name="AuditWorkflow",

    sub_agents=[
        extraction_agent,
        compliance_agent,
        verification_agent,
        report_agent
    ]

)