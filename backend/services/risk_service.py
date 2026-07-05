def calculate_risk(findings) : 

    high = 0 
    medium = 0 

    for finding in findings : 

        severity = finding.get("severity")

        if severity == "High" : 
            high = high + 1 
        
        elif severity == "Medium" : 
            medium = medium + 1 
        
    if high >= 2 : 
        return "High"
    
    elif high == 1 and medium >= 2 : 
        return "Medium" 
    
    return "Low"