from anomaly.check_anomalies import check_anomalies
from services.risk_service import calculate_risk
from database import save_audit_logs, save_invoice

def run_audit_pipeline(invoice: dict):

    anomalies = check_anomalies(invoice)

    save_invoice(invoice)

    risk = calculate_risk(anomalies)

    save_audit_logs(invoice.get("invoice_number"), len(anomalies), risk)

    return {
        "status": "Completed",
        "invoice": invoice,
        "findings": anomalies,
        "summary": {
            "total_issues": len(anomalies),
            "risk": risk
        }
    }


