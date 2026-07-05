from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_FOLDER = Path("reports")
OUTPUT_FOLDER.mkdir(exist_ok=True)


def heading(text):

    return Paragraph(
        text,
        ParagraphStyle(
            "Heading",
            fontName="Helvetica-Bold",
            fontSize=15,
            textColor=colors.darkblue,
            spaceAfter=10,
            spaceBefore=18,
        ),
    )


def normal(text):

    return Paragraph(
        str(text),
        ParagraphStyle(
            "Normal",
            fontName="Helvetica",
            fontSize=10,
            leading=16,
        ),
    )


def generate_pdf(report):

    invoice = report["invoice"]
    findings = report["findings"]
    compliance = report["compliance"]
    verification = report["verification"]

    invoice_number = invoice.get("invoice_number", "Unknown")

    pdf_path = OUTPUT_FOLDER / f"Audit_Report_{invoice_number}.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    story = []

    # TITLE

    title_style = ParagraphStyle(
    "AuditTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=26,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#003366"),
    spaceAfter=8,
)

    subtitle_style = ParagraphStyle(
        "AuditSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=14,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=25,
    )

    story.append(Paragraph("AuditIQ", title_style))
    story.append(Paragraph("AI Invoice Audit Report", subtitle_style))

    story.append(Spacer(1, 0.35 * inch))

    # Invoice Details

    story.append(heading("Invoice Details"))

    invoice_table = Table(
        [
            ["Invoice Number", invoice.get("invoice_number", "")],
            ["Vendor", invoice.get("vendor", "")],
            ["Amount", f"₹ {invoice.get('amount', '')}"],
            ["Invoice Date", invoice.get("date", "")],
            ["GST", f"₹ {invoice.get('gst', '')}"],
        ],
        colWidths=[180, 300],
    )

    invoice_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2FF")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(invoice_table)

    story.append(heading("Database Validation"))

    checks = []

    duplicate = any(
        f["rule"] == "Duplicate Invoice"
        for f in findings
    )

    checks.append([
        "Duplicate Invoice Check",
        "FAILED" if duplicate else "PASSED"
    ])

    vendor = any(
        "Vendor" in f["rule"]
        for f in findings
    )

    checks.append([
        "Vendor Verification",
        "FAILED" if vendor else "PASSED"
    ])

    db_table = Table(
        [["Validation", "Result"]] + checks,
        colWidths=[320,160]
    )

    db_table.setStyle(
        TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),0.5,colors.grey),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ])
    )

    story.append(db_table)

    # Findings

    story.append(heading("Anomaly Detection"))

    summary = report["summary"]

    story.append(normal(f"Total Findings : {summary['total_findings']}"))
    story.append(normal(f"High : {summary['high']}"))
    story.append(normal(f"Medium : {summary['medium']}"))
    story.append(normal(f"Low : {summary['low']}"))

    story.append(Spacer(1, 0.2 * inch))

    severity_colors = {
        "High": colors.red,
        "Medium": colors.orange,
        "Low": colors.green,
    }

    for i, finding in enumerate(findings, start=1):

        severity = finding.get("severity", "Low")

        card = Table(
            [
                ["Finding", str(i)],
                ["Rule", finding.get("rule")],
                ["Severity", severity],
                ["Message", finding.get("message")],
                ["Evidence", str(finding.get("evidence"))],
            ],
            colWidths=[120, 360],
        )

        card.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                    ("TEXTCOLOR", (1, 2), (1, 2), severity_colors.get(severity, colors.black)),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        story.append(card)
        story.append(Spacer(1, 0.15 * inch))

    # Compliance

    story.append(heading("Compliance"))

    story.append(normal(f"<b>Status:</b> {compliance.get('status')}"))

    violations = compliance.get("violations", [])

    if violations:

        for violation in violations:
            story.append(normal(f"• {violation}"))

    else:
        story.append(normal("No compliance violations detected."))

    # Verification

    story.append(heading("Verification"))

    verification_table = Table(
        [
            ["Verified", str(verification.get("verified", "-"))],
            ["Decision", verification.get("decision", "-")],
            ["Overall Risk", verification.get("overall_risk", "-")],
            ["Risk Score", str(verification.get("risk_score", "-"))],
            ["Confidence", f"{verification.get('confidence', '-')} %"],
        ],
        colWidths=[180, 300],
    )

    verification_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF7EE")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ]
        )
    )

    story.append(verification_table)

    # Final Decision

    story.append(heading("Final Decision"))

    decision = report["final_decision"]

    if decision == "APPROVE":

        bg = colors.green

    elif decision == "REVIEW":

        bg = colors.orange

    else:

        bg = colors.red

    decision_table = Table(
        [[decision]],
        colWidths=[480],
    )

    decision_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 18),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    story.append(heading("Recommended Action"))

    decision = report["final_decision"]

    if decision == "APPROVE":

        action = "Invoice can be processed for payment."

    elif decision == "REVIEW":

        action = "Manual review by Finance Team is recommended."

    else:

        action = "Reject the invoice and investigate before payment."

    story.append(normal(action))

    story.append(decision_table)

    story.append(Spacer(1, 0.2 * inch))

    story.append(normal(f"<b>Reason:</b> {report['reason']}"))


    story.append(heading("Workflow Execution"))

    workflow = [
        ["Extraction Agent", "Completed"],
        ["Anomaly Detection", "Completed"],
        ["Compliance Agent", "Completed"],
        ["Verification Agent", "Completed"],
        ["Report Generator", "Completed"],
    ]

    table = Table(
        [["Stage","Status"]]+workflow,
        colWidths=[280,200]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),0.5,colors.grey),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ])
    )

    story.append(table)

    story.append(Spacer(1, 0.4 * inch))

    story.append(
        Paragraph(
            f"Generated by AuditIQ<br/>Generated on {datetime.now().strftime('%d %B %Y %H:%M:%S')}",
            ParagraphStyle(
                "Footer",
                alignment=TA_CENTER,
                textColor=colors.grey,
                fontSize=9,
            ),
        )
    )

    doc.build(story)

    return str(pdf_path)