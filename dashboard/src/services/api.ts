export async function runAudit(url:string){

  const res = await fetch("http://127.0.0.1:8000/audit",{
    method:"POST",
    headers:{ "Content-Type":"application/json"},
    body:JSON.stringify({url})
  })

  return res.json()
}

export async function getResult(jobId:string){

  const r = await fetch(`http://127.0.0.1:8000/result/${jobId}`)

  return r.json()
}

export async function askAI(jobId:string, question:string){

  const res = await fetch("http://127.0.0.1:8000/explain",{
    method:"POST",
    headers:{ "Content-Type":"application/json"},
    body:JSON.stringify({job_id:jobId, question})
  })

  return res.json()
}
