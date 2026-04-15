
from fastapi import APIRouter

router = APIRouter()

@router.post("/anonymous")
def anonymous_report(report: dict):
    return {"status": "Anonymous report submitted"}
