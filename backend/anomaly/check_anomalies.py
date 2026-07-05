from anomaly.invoice_rules import (check_negative_amount, 
                                            check_missing_vendor, 
                                            check_missing_invoice_no, 
                                            check_missing_gst, 
                                            check_future_date,
                                            check_duplicate_invoice,
                                            check_vendor_approval,
                                            check_po_exists,
                                            check_po_amount,
                                            check_duplicate_payment,
                                            check_split_invoice)

def check_anomalies(invoice: dict) : 

    anomalies = [] 

    rules = [check_negative_amount, 
            check_missing_vendor, 
            check_missing_invoice_no, 
            check_missing_gst, 
            check_future_date,
            check_duplicate_invoice,
            check_vendor_approval,
            check_po_exists,
            check_po_amount,
            check_duplicate_payment,
            check_split_invoice] 

    for rule in rules : 
        
        result = rule(invoice) 
        
        if result is not None:
            anomalies.append(result)

    return anomalies 