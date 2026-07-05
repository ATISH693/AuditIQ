from google.adk.tools import ToolContext
from anomaly.check_anomalies import check_anomalies
from utils.logger import logger


def run_anomaly_detection(tool_context: ToolContext):
    """
    Direct anomaly detection step 
    """

    logger.info("Anomaly detection started.")

    invoice = tool_context.state.get("invoice")

    if not invoice:
        logger.error("No invoice found in state.")
        return []

    # Run deterministic anomaly logic
    findings = check_anomalies(invoice)

    # Store in shared state
    tool_context.state["findings"] = findings

    logger.info(f"Detected {len(findings)} anomalies.")

    return findings