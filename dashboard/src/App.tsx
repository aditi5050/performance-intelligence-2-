import { useState } from "react"
import MetricCard from "./components/MetricCard"
import SuggestionCard from "./components/SuggestionCard"
import ChatBox from "./components/ChatBox"
import { runAudit, getResult } from "./services/api"

export default function App(){

 const [url,setUrl]=useState("")
 const [result,setResult]=useState(null)
 const [jobId,setJobId]=useState(null)

 async function analyze(){

   const res = await runAudit(url)

   setJobId(res.job_id)

   const interval=setInterval(async()=>{

     const data = await getResult(res.job_id)

     if(!data.status){

       setResult(data)
       clearInterval(interval)

     }

   },2000)
 }

 return(

  <div>

    <input value={url} onChange={(e)=>setUrl(e.target.value)} />

    <button onClick={analyze}>Analyze</button>

    {result &&(

      <>

        <h2>{result.performance_score}</h2>

        <MetricCard title="LCP" value={result.lcp}/>

        {result.suggestions.map((s,i)=>(

          <SuggestionCard key={i} suggestion={s}/>

        ))}

        <ChatBox jobId={jobId}/>

      </>

    )}

  </div>

 )
}
