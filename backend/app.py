from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

from backend.finrobot_service import analyze_company
from backend.llm_agent import explain

app = FastAPI(title="FinRobot Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    company: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    metrics = analyze_company(req.company)

    try:
        explanation = explain(metrics)
    except Exception:
        explanation = "LLM explanation unavailable."

    return {
        "decision": metrics["decision"],
        "metrics": metrics,
        "explanation": explanation
    }
