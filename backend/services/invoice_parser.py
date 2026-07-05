from backend.services.extraction_llm import ask_llm 
import re 

def extract_with_python(text: str) : 

    data = {}

    invoice = re.search(r"Invoice Number:\s*(.+)", text)
    vendor = re.search(r"Vendor:\s*(.+)", text)
    amount = re.search(r"Amount:\s*(.+)", text)

    if invoice:
        data["invoice_number"] = invoice.group(1)

    if vendor:
        data["vendor"] = vendor.group(1)

    if amount:
        data["amount"] = amount.group(1)

    return data


def check_missing_fields(data: dict) : 

    missing_fields = []
    required = ["invoice_number", "vendor", "amount", "date", "gst"]

    for field in required : 
        
        if not data.get(field):
            
            missing_fields.append(field)
    
    return missing_fields 


def extract_data(text: str) : 

    data = extract_with_python(text) 

    missing = check_missing_fields(data)

    if len(missing) == 0 : 
        return {"source" : "python" , "data" : data}

    else : 
        llm_data = ask_llm(text) 
        return {"source" : "llm", "missing_fields": missing, "data" : llm_data}  


