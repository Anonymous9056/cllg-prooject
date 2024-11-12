from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from db.base import get_db

router = APIRouter()

@router.get("/live")
async def liveness_check():
    """Basic health check endpoint."""
    return {"status": "ok"}

@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Check if the application is ready to handle requests."""
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "database": db_status,
    }