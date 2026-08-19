from typing import Dict, Any
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import CopilotChatRequest, CopilotChatResponse
from app.services.copilot_service import copilot_service, INDIAN_LANGUAGES

router = APIRouter()

@router.get("/languages", summary="List all 22 Official Scheduled Indian Languages + English")
async def get_supported_languages():
    """
    Returns the supported Indian languages with their English names, native script names, and flags.
    """
    return INDIAN_LANGUAGES

@router.post("/chat", response_model=CopilotChatResponse, summary="Multilingual Citizen Copilot Chat (All Indian Languages)")
async def copilot_chat(req: CopilotChatRequest):
    """
    Direct low-latency AI conversation for passport guidance, fee clarification,
    and eligibility checks across all Indian languages.
    """
    return await copilot_service.get_response(req)

@router.post("/stream", summary="Streaming Real-Time Citizen Copilot (SSE)")
async def copilot_stream(req: CopilotChatRequest):
    """
    Server-Sent Events (SSE) streaming endpoint for immediate first-token delivery (<200ms).
    """
    return StreamingResponse(
        copilot_service.stream_response(req),
        media_type="text/event-stream"
    )
