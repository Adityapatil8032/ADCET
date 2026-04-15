
from fastapi import FastAPI
from routes import jobs, workers, reports
from services.ai_service import get_fair_wage_estimate

app = FastAPI(title="FairWage API")

app.include_router(jobs.router, prefix="/jobs")
app.include_router(workers.router, prefix="/workers")
app.include_router(reports.router, prefix="/reports")

@app.get("/")
def root():
    return {"message": "FairWage API Running"}
