import redis
import json
import subprocess

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("Worker started...")

while True:

    job = r.blpop("audit_queue")

    if job:
        data = json.loads(job[1])
        job_id = data["id"]
        url = data["url"]

        print("Running audit for:", url)

        result = subprocess.run(
            ["node", "./runAudit.js", url],
            capture_output=True,
            text=True
        )

        r.set(f"result:{job_id}", result.stdout)

        print("Saved result for job:", job_id)
