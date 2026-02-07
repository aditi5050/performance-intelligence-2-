from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import json
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# ==============================
# REQUEST MODELS
# ==============================

class AuditRequest(BaseModel):
    url: str

class ExplainRequest(BaseModel):
    job_id: str
    question: str

# ==============================
# AI ENGINE
# ==============================

def generate_reasoned_answer(data, question):

    q = question.lower()
    response = []

    if "wrong" in q or "problem" in q:
        if data.get("lcp",0) > 4000:
            response.append("Main content loads very late (High LCP).")
        if data.get("tbt",0) > 300:
            response.append("Heavy JavaScript blocks interaction.")

    if "slow" in q:
        response.append(f"LCP = {data.get('lcp')}ms indicates slow rendering.")

    if "traffic" in q:
        response.append("High traffic may worsen performance due to heavy assets.")

    if "fix" in q:
        suggestions = data.get("suggestions",[])
        if suggestions:
            best = suggestions[0]
            response.append(f"Best fix: {best['issue']} → {best['fix']}")

    if "code" in q:
        response.append("<img loading='lazy'> or dynamic React imports.")

    if not response:
        response.append("Performance mainly affected by rendering and JS blocking.")

    return " ".join(response)

# ==============================
# CREATE AUDIT JOB
# ==============================

@app.post("/audit")
def run_audit(data: AuditRequest):

    job_id = str(uuid.uuid4())

    job_data = {
        "id": job_id,
        "url": data.url
    }

    r.rpush("audit_queue", json.dumps(job_data))

    return {
        "message": "Job added",
        "job_id": job_id
    }

# ==============================
# GET RESULT
# ==============================

@app.get("/result/{job_id}")
def get_result(job_id: str):

    result = r.get(f"result:{job_id}")

    if result:
        return json.loads(result)

    return {"status":"processing"}

# ==============================
# GET HISTORY
# ==============================

@app.get("/history")
def get_history(url: str):

    history = r.lrange(f"history:{url}",0,-1)

    return [json.loads(h) for h in history]

# ==============================
# AI EXPLAIN ENDPOINT
# ==============================

@app.post("/explain")
def explain(req: ExplainRequest):

    result = r.get(f"result:{req.job_id}")

    if not result:
        return {"error":"job not found"}

    data = json.loads(result)

    answer = generate_reasoned_answer(data, req.question)

    return {"answer":answer}
