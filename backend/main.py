from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import uuid

app = FastAPI()

# connect redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# request schema
class AuditRequest(BaseModel):
    url: str


# create audit job
@app.post("/audit")
def run_audit(data: AuditRequest):

    job_id = str(uuid.uuid4())

    job_data = {
        "id": job_id,
        "url": data.url
    }

    # push job to queue
    r.rpush("audit_queue", json.dumps(job_data))

    return {
        "message": "Job added",
        "job_id": job_id
    }


# get audit result
@app.get("/result/{job_id}")
def get_result(job_id: str):

    result = r.get(f"result:{job_id}")

    if result:
        return json.loads(result)

    return {"status": "processing"}


# get history
@app.get("/history")
def get_history(url: str):

    history = r.lrange(f"history:{url}", 0, -1)

    return [json.loads(h) for h in history]
