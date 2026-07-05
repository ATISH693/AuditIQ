import psycopg2

def get_connection():

    conn = psycopg2.connect(
        dbname="auditiq",
        user="postgres",
        password="Dh@nu@09",
        host="localhost",
        port="5432"
    )

    return conn 

def invoice_exists(invoice_number: str) -> bool: 

    conn = get_connection() 
    cur = conn.cursor() 

    cur.execute(
        """
        SELECT 1 FROM invoices 
        WHERE invoice_number = %s 
        LIMIT 1
        """,
        (invoice_number,)
    )

    result = cur.fetchone()

    cur.close()
    conn.close() 

    if result is not None : 
        return True 
    
    return False

def vendor_exists(vendor: str) -> bool : 

    conn = get_connection() 
    cur = conn.cursor() 

    cur.execute(
        """
        SELECT 1 FROM approved_vendors
        WHERE vendor_name = %s
        LIMIT 1
        """,
        (vendor,)
    )
    
    result = cur.fetchone()
    
    cur.close() 
    conn.close() 

    if result is not None : 
        return True 
    
    return False 

def po_exists(po_number: str) -> bool:

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM purchase_orders
        WHERE po_number = %s
        LIMIT 1
        """,
        (po_number,)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is not None: 
        return True 
    
    return False

def get_po_amount(po_number: str) -> float:


    conn = get_connection()
    cur = conn.cursor() 

    cur.execute(
        """
        SELECT approved_amount FROM purchase_orders 
        WHERE po_number = %s
        """,
        (po_number,)
    )

    result = cur.fetchone()
    
    cur.close()
    conn.close()

    if result is None:
        return None

    return result[0]

def duplicate_payment_exists(vendor: str, amount: float, invoice_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM invoices
        WHERE vendor = %s
        AND amount = %s
        AND invoice_date = %s
        LIMIT 1
        """,
        (vendor, amount, invoice_date)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is not None :
        return True 
    
    return False 

def get_total_invoice_amount(vendor: str, invoice_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT SUM(amount) FROM invoices 
        WHERE vendor = %s AND invoice_date = %s
        """,
        (vendor, invoice_date)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result[0] is  None :
        return None

    return result[0]

def save_invoice(invoice: dict):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO invoices (
                invoice_number,
                vendor,
                amount,
                invoice_date,
                gst,
                po_number
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                invoice.get("invoice_number"),
                invoice.get("vendor"),
                invoice.get("amount"),
                invoice.get("date"),
                invoice.get("gst"),
                invoice.get("po_number")
            )
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("DB Error:", e)

    finally:
        cur.close()
        conn.close()

def save_audit_logs(invoice_number:str, total_issues:int, risk:str) : 

    conn = get_connection() 
    cur = conn.cursor() 

    cur.execute(
        """
        INSERT INTO audit_logs (invoice_number, total_issues, risk) 
        VALUES (%s,%s,%s) 
        """,
        (invoice_number, total_issues, risk)
    )

    conn.commit()

    cur.close()
    conn.close()
