import redis
import json
import subprocess

# connect redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("Worker started...")


# ==============================
# SMART INSIGHTS ENGINE
# ==============================
def generate_insights(data):

    insights = []

    if data["performance_score"] < 50:
        insights.append("⚠️ Performance score very low — heavy optimization needed")

    if data["lcp"] > 4000 and data["performance_score"] < 80:
        insights.append(
            f"⚠️ LCP too high ({data['lcp']:.0f}ms) — optimize images or reduce render blocking resources"
        )

    if data["cls"] > 0.1:
        insights.append("⚠️ Layout shifts detected — fix CLS issues")

    if data["tbt"] > 300:
        insights.append("⚠️ High Total Blocking Time — reduce heavy JS execution")

    return insights



# ==============================
# REGRESSION DETECTION 😈
# ==============================
def detect_regression(url, new_result):

    history_key = f"history:{url}"

    history = r.lrange(history_key, -2, -1)

    if len(history) == 2:

        prev = json.loads(history[0])
        curr = new_result

        diff = curr["performance_score"] - prev["performance_score"]

        if diff < -5:
            return f"🚨 Performance dropped by {abs(diff)} points"

    return None


# ==============================
# WORKER LOOP
# ==============================
while True:

    job = r.blpop("audit_queue")

    if job:

        data = json.loads(job[1])

        job_id = data["id"]
        url = data["url"]

        print("Running audit for:", url)

        result = subprocess.run(
            ["node", "runAudit.js", url],
            capture_output=True,
            text=True
        )

        print("NODE OUTPUT:", result.stdout)

        result_json = json.loads(result.stdout)

        # add insights
        result_json["insights"] = generate_insights(result_json)

        # detect regression
        alert = detect_regression(url, result_json)

        if alert:
            result_json["alert"] = alert
            print(alert)

        final_result = json.dumps(result_json)

        # save result
        r.set(f"result:{job_id}", final_result)

        # save history
        history_key = f"history:{url}"
        r.rpush(history_key, final_result)

        print("Saved result for job:", job_id)
