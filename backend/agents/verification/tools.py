from google.adk.tools import ToolContext
from utils.logger import logger


def verify_audit(tool_context: ToolContext):

    # Prevent re-execution
    if tool_context.state.get("verification_done"):
        return tool_context.state["verification"]

    invoice = tool_context.state.get("invoice", {})
    findings = tool_context.state.get("findings", [])
    compliance = tool_context.state.get("compliance", {"status": "Unknown"})

    # Risk Scoring Model
    severity_weights = {
        "High": 40,
        "Medium": 20,
        "Low": 10
    }

    risk_score = 0
    high = medium = low = 0

    for finding in findings:

        severity = finding.get("severity", "Low")
        risk_score += severity_weights.get(severity, 10)

        if severity == "High":
            high += 1
        elif severity == "Medium":
            medium += 1
        else:
            low += 1

    # Compliance impact (IMPORTANT: stronger weight)
    if compliance.get("status") == "Failed":
        risk_score += 30

    # Risk Level
    if risk_score >= 80:
        overall_risk = "Critical"
    elif risk_score >= 50:
        overall_risk = "High"
    elif risk_score >= 20:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"

    # Confidence Score
    confidence = 100

    required_fields = ["invoice_number", "vendor", "amount", "date", "gst"]

    for field in required_fields:
        value = invoice.get(field)
        if value is None or value == "":
            confidence -= 10

    # compliance reduces confidence
    if compliance.get("status") == "Failed":
        confidence -= 10

    # more findings = less confidence
    confidence -= len(findings) * 3

    confidence = max(min(confidence, 100), 0)

    # FINAL DECISION (FIXED LOGIC)

    # RULE 1: Compliance failure always forces REVIEW minimum
    if compliance.get("status") == "Failed":
        if overall_risk in ["High", "Critical"]:
            decision = "REJECT"
        else:
            decision = "REVIEW"

    # RULE 2: High risk overrides everything
    elif overall_risk in ["Critical", "High"]:
        decision = "REJECT"

    # RULE 3: Low confidence forces manual review
    elif confidence < 80:
        decision = "REVIEW"

    else:
        decision = "APPROVE"

    # Verified flag (FIXED MEANING)
    verified = decision == "APPROVE"

    # -----------------------------
    # Result
    # -----------------------------
    result = {
        "verified": verified,
        "decision": decision,
        "confidence": confidence,
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "summary": {
            "high_findings": high,
            "medium_findings": medium,
            "low_findings": low
        }
    }

    tool_context.state["verification"] = result
    tool_context.state["verification_done"] = True

    logger.info("Verification completed.")

    return result