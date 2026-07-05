import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from backend.agents.workflow import audit_workflow
from backend.utils.logger import logger

APP_NAME = "AuditIQ"

# Create ONE session service for the whole application
session_service = InMemorySessionService()

# Create ONE runner for the whole application
runner = Runner(
    app_name=APP_NAME,
    agent=audit_workflow,
    session_service=session_service,
)


async def run_audit_workflow(pdf_text: str):

    user_id = "default_user"
    session_id = str(uuid.uuid4())

    # Create a session and initialize the state
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state={
            "pdf_text": pdf_text
        }
    )

    # Initial prompt
    content = types.Content(
        role="user",
        parts=[
            types.Part(text="Extract the invoice information from the PDF text stored in the session state by calling the extraction tool.")
        ]
    )

    logger.info("Starting ADK workflow.")

    # Execute the workflow
    async for event in runner.run_async(
    user_id=user_id,
    session_id=session_id,
    new_message=content,
):
        pass

    # Retrieve the updated session
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    logger.info("Workflow finished successfully.")

    return {
        "invoice": session.state.get("invoice"),
        "findings": session.state.get("findings"),
        "compliance": session.state.get("compliance"),
        "verification": session.state.get("verification"),
        "report": session.state.get("report"),
    }
