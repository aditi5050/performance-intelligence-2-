import { useState } from "react"
import { askAI } from "../services/api"

export default function ChatBox({jobId}){

 const [messages,setMessages]=useState([])
 const [input,setInput]=useState("")

 async function send(){

  const res = await askAI(jobId,input)

  setMessages([
    ...messages,
    {role:"user",text:input},
    {role:"ai",text:res.answer}
  ])

  setInput("")
 }

 return(

  <div>

    <h3>Ask PerfAI</h3>

    <div>

      {messages.map((m,i)=>(

        <p key={i}>{m.text}</p>

      ))}

    </div>

    <input value={input} onChange={(e)=>setInput(e.target.value)} />

    <button onClick={send}>Ask</button>

  </div>

 )
}
