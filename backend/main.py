from fastapi import FastAPI, UploadFile, File, HTTPException
from audit_adk.runner import run_audit_workflow
from services.extraction_service import extract_pdf_text
from utils.logger import logger
from services.invoice_classifier import is_invoice
from fastapi.responses import FileResponse
from pathlib import Path
app = FastAPI() 

@app.get("/") 
def mypage() : 
    return {"message" : "Welcome to our page"} 


@app.post("/audit_upload")
async def upload_pdf(file: UploadFile = File(...)):

    logger.info("API HIT: | request received")

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    logger.info("Received PDF upload.")
    
    #Check 1
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415 , detail = "Only PDF files allowed")
    
    #Check
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size must be less than 10 MB.")
    file.file.seek(0)  

    extracted_text = extract_pdf_text(file.file)

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF. Maybe it is Empty")
    
    print(extracted_text)

    if not is_invoice(extracted_text):
        raise HTTPException(status_code= 404, detail= "Uploaded Document is not an invoice")

    logger.info("PDF text extracted successfully.")

    audit_result = await run_audit_workflow(extracted_text)

    return audit_result 
 

@app.get("/reports/{filename}")
def download_report(filename: str):

    path = Path("reports") / filename

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)