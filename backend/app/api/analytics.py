from fastapi import APIRouter

from app.services.feedback_analyzer import analyze_feedback

router = APIRouter()


@router.get("/analytics")
async def analytics():

    return analyze_feedback()