from datetime import date, datetime
from database import invoice_exists, vendor_exists, po_exists, get_po_amount, duplicate_payment_exists, get_total_invoice_amount

def check_negative_amount(invoice: dict) : 

    amount = invoice.get("amount") 

    if amount is None : 
        return None 
    
    else :
        if amount < 0 : 
            
            return {
                "rule": "Negative Amount",
                "severity": "High",
                "message": "Invoice amount cannot be negative.",
                "evidence": {
                    "amount": amount
                    }
            } 
    
    return None

def check_missing_vendor(invoice: dict) : 

    vendor = invoice.get("vendor") 

    if not vendor : 
        
        return {
            "rule": "Missing Vendor",
            "severity": "High",
            "message": "Vendor name is missing.",
            "evidence": {}
        }
    
    return None

def check_missing_invoice_no(invoice: dict) : 

    invoice_no = invoice.get("invoice_number") 

    if not invoice_no : 
        
        return {
            "rule": "Missing Invoice No",
            "severity": "High",
            "message": "Invoice number is missing.",
            "evidence": {}
        }
    
    return None

def check_missing_gst(invoice: dict) : 

    gst = invoice.get("gst") 

    if not gst : 
        
        return {
            "rule": "Missing GST",
            "severity": "Medium",
            "message": "GST Amount is missing.",
            "evidence": {}
        }
    
    return None

def check_future_date(invoice: dict):

    invoice_date = invoice.get("date")

    if invoice_date is None:
        return None
    
    invoice_date = datetime.strptime(invoice_date, "%Y-%m-%d").date()

    if invoice_date > date.today():

        return {
            "rule": "Future Invoice Date",
            "severity": "Medium",
            "message": "Invoice date is in the future.",
            "evidence": {
                "invoice_date": str(invoice_date)
            }
        }

    return None

def check_duplicate_invoice(invoice: dict) : 

    invoice_number = invoice.get("invoice_number")

    if invoice_number is None:
        return None

    if invoice_exists(invoice_number) : 
        return {
            "rule": "Duplicate Invoice",
            "severity": "High",
            "message": "Invoice number already exists in the database.",
            "evidence": {
                "invoice_number": invoice_number
            }
        }

    return None

def check_vendor_approval(invoice: dict) : 
    
    vendor = invoice.get("vendor") 

    if vendor is None :
        return None 

    if not vendor_exists(vendor) : 
        
        return {
            "rule": "Vendor Validation",
            "severity": "High",
            "message": "Vendor is not in the approved vendors list.",
            "evidence": {
                "vendor": vendor
            }
        }
    
    return None

def check_po_exists(invoice: dict) : 

    po_number = invoice.get("po_number") 

    if po_number is None : 
        return None 

    if not po_exists(po_number): 
        
        return {
            "rule": "Purchase Order Validation",
            "severity": "High",
            "message": "Purchase Order does not exist.",
            "evidence": {
                "po_number": po_number
            }
        }

    return None

def check_po_amount(invoice: dict) : 

    po_number = invoice.get("po_number") 
    invoice_amount = invoice.get("amount")

    if not po_number or invoice_amount is None :
        return None 
    
    approved_amount = get_po_amount(po_number)

    if approved_amount is None:
        return None

    if invoice_amount > approved_amount: 
        
        return {
            "rule": "PO Amount Mismatch",
            "severity": "High",
            "message": "Invoice amount exceeds the approved PO amount.",
            "evidence": {
                "invoice_amount": invoice_amount,
                "approved_amount": approved_amount,
                "difference": invoice_amount - approved_amount
            }
        }

    return None

def check_duplicate_payment(invoice: dict):

    vendor = invoice.get("vendor")
    amount = invoice.get("amount")
    invoice_date = invoice.get("invoice_date")

    if not vendor or amount is None or invoice_date is None:
        return None

    if duplicate_payment_exists(vendor, amount, invoice_date):

        return {
            "rule": "Duplicate Payment",
            "severity": "High",
            "message": "Possible duplicate payment detected.",
            "evidence": {
                "vendor": vendor,
                "amount": amount,
                "invoice_date": invoice_date
            }
        }

    return None

APPROVAL_LIMIT = 50000

def check_split_invoice(invoice: dict):

    vendor = invoice.get("vendor")
    invoice_date = invoice.get("invoice_date")
    amount = invoice.get("amount")

    if not vendor or invoice_date is None or amount is None:
        return None

    total = get_total_invoice_amount(vendor, invoice_date)

    total += amount

    if total > APPROVAL_LIMIT:

        return {
            "rule": "Split Invoice",
            "severity": "Medium",
            "message": "Possible invoice splitting detected.",
            "evidence": {
                "vendor": vendor,
                "total_amount": total,
                "approval_limit": APPROVAL_LIMIT
            }
        }

    return None