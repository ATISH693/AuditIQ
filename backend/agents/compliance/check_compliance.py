from services.rag.retriever import retrieve_documents


def check_compliance(invoice: dict):

    query = f"""
    Check compliance for this invoice.

    Vendor: {invoice.get("vendor")}
    Amount: {invoice.get("amount")}
    GST: {invoice.get("gst")}
    Date: {invoice.get("date")}
    """

    documents = retrieve_documents(query,1)

    policy_context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    return policy_context