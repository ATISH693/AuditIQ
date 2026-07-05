import os
import requests
import gradio as gr

API_URL = "http://127.0.0.1:8000/audit_upload"


def audit_invoice(pdf):

    if pdf is None:
        raise gr.Error("Please upload a PDF.")

    with open(pdf.name, "rb") as f:
        response = requests.post(
            API_URL,
            files={"file": (os.path.basename(pdf.name), f, "application/pdf")}
        )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        raise gr.Error(response.text)

    result = response.json()

    invoice = result.get("invoice", {})
    findings = result.get("findings", [])
    compliance = result.get("compliance", {})
    verification = result.get("verification", {})
    report = result.get("report", {})

    # ---------------- Invoice ----------------
    invoice_text = f"""
Invoice Number : {invoice.get("invoice_number", "-")}
Vendor         : {invoice.get("vendor", "-")}
Amount         : ₹{invoice.get("amount", "-")}
Invoice Date   : {invoice.get("date", "-")}
GST            : ₹{invoice.get("gst", "-")}
"""

    # ---------------- Anomaly ----------------
    summary = report.get("summary", {})

    anomaly_text = f"""
🔴 High   : {summary.get("high", 0)}
🟠 Medium : {summary.get("medium", 0)}
🟢 Low    : {summary.get("low", 0)}

Total Findings : {summary.get("total_findings", 0)}
"""

    # ---------------- Compliance ----------------
    compliance_text = f"""
Status : {compliance.get("status", "-")}

Violations:
{chr(10).join(compliance.get("violations", []))}
"""

    # ---------------- Verification ----------------
    verification_text = f"""
Verified   : {verification.get("verified")}

Confidence : {verification.get("confidence")} %

Risk       : {verification.get("overall_risk")}
"""

    # ---------------- Decision ----------------
    decision_text = f"""
Decision : {report.get("final_decision", "-")}

Reason :

{report.get("reason", "")}
"""

    # ---------------- PDF DOWNLOAD ----------------
    pdf_url = report.get("pdf_url")

    download_html = f"""
    <a href="{pdf_url}" target="_blank" style="
        display:inline-block;
        padding:10px 15px;
        background:#2563eb;
        color:white;
        text-decoration:none;
        border-radius:6px;
        font-weight:bold;
    ">
    📥 Download Audit Report
    </a>
    """

    return (
        invoice_text,
        anomaly_text,
        compliance_text,
        verification_text,
        decision_text,
        download_html,
    )


# ---------------- UI ----------------
with gr.Blocks(title="AuditIQ") as demo:

    gr.Markdown("""
# 🧾 AuditIQ
### AI Powered Invoice Auditing System
""")

    pdf = gr.File(label="Upload Invoice", file_types=[".pdf"])
    audit_btn = gr.Button("Audit Invoice", variant="primary")

    with gr.Row():
        invoice_box = gr.Textbox(label="Invoice Details", lines=7)
        anomaly_box = gr.Textbox(label="Anomaly Summary", lines=7)

    with gr.Row():
        compliance_box = gr.Textbox(label="Compliance", lines=7)
        verification_box = gr.Textbox(label="Verification", lines=7)

    decision_box = gr.Textbox(label="Final Decision", lines=6)

    download_box = gr.HTML()

    audit_btn.click(
        fn=audit_invoice,
        inputs=pdf,
        outputs=[
            invoice_box,
            anomaly_box,
            compliance_box,
            verification_box,
            decision_box,
            download_box,
        ],
    )

demo.launch()