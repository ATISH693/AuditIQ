from google.adk.tools import ToolContext
from backend.services.report_generator import generate_report
from backend.utils.logger import logger
from backend.services.pdf_generator import generate_pdf
from backend.database import save_audit_logs
from pathlib import Path

def create_audit_report(tool_context: ToolContext):

    """
    Create the final audit report.
    """

    logger.info("Generating audit report.")

    invoice = tool_context.state.get("invoice", {})

    findings = tool_context.state.get("findings", [])

    compliance = tool_context.state.get("compliance", {})

    verification = tool_context.state.get("verification", {})

    report = generate_report(
        invoice=invoice,
        findings=findings,
        compliance=compliance,
        verification=verification
    )

    pdf_path = generate_pdf(report)

    filename = Path(pdf_path).name

    report["pdf_name"] = filename
    
    tool_context.state["report"] = report

    logger.info("Audit report generated successfully.")

    save_audit_logs(
        invoice.get("invoice_number"),
        len(findings),
        verification.get("overall_risk")
    )

    return report