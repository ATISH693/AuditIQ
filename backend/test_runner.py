import asyncio
from audit_adk.runner import run_audit_workflow

pdf_text = """
==================== TAX INVOICE ====================

Invoice Number : INV-2058
Invoice Date   : 2026-07-03

Vendor Name    : XYZ Office Supplies Pvt. Ltd.
GSTIN          : 27ABCDE1234F1Z5

Bill To
TechNova Solutions Pvt. Ltd.

------------------------------------------------------

Items

1. Office Chairs (10)        ₹ 35,000
2. Office Desks (5)          ₹ 40,000
3. Monitors (4)              ₹ 25,000

------------------------------------------------------

Subtotal                      ₹ 100,000
GST (18%)                     ₹ 18,000

Total Amount                  ₹ 118,000

Payment Terms:
Net 30 Days

Bank:
ABC Bank

Thank you for your business.

======================================================
"""


async def main():

    result = await run_audit_workflow(pdf_text)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())