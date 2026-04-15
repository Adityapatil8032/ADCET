
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_jobs():
    return {"jobs": []}

@router.post("/create")
def create_job(job: dict):
    return {"status": "Job created", "job": job}
