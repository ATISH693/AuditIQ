from google.adk.tools import ToolContext
from backend.agents.compliance.check_compliance import check_compliance
from backend.utils.logger import logger
from backend.agents.anomaly.tools import run_anomaly_detection

def check_invoice_compliance(tool_context: ToolContext):

    if tool_context.state.get("compliance_checked"):
        return tool_context.state.get("compliance_cached_result")

    if "findings" not in tool_context.state:
        run_anomaly_detection(tool_context)

    invoice = tool_context.state["invoice"]

    policy_context = check_compliance(invoice)

    result = {
        "policy_context": policy_context
    }

    tool_context.state["compliance_checked"] = True
    tool_context.state["compliance_cached_result"] = result

    return result

def save_compliance_result(status: str, violations: list, tool_context: ToolContext):

    if tool_context.state.get("compliance_saved"):
        return tool_context.state["compliance"]

    result = {
        "status": status,
        "violations": violations
    }

    tool_context.state["compliance"] = result
    tool_context.state["compliance_saved"] = True

    logger.info("Compliance check completed.")

    return result