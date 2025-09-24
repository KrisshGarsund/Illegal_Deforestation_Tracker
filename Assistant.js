import React, { useState } from "react";
import API from "./api";

export default function Assistant({token}){
  const [q, setQ] = useState("");
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    if(!token){ setAnswer("Please login to use assistant."); return; }
    const res = await fetch(`/api/assistant`, {
      method: "POST",
      headers: {"Content-Type":"application/json", "Authorization": `Bearer ${token}`},
      body: JSON.stringify({question: q})
    });
    const j = await res.json();
    setAnswer(j.reply || j.answer || JSON.stringify(j));
  };

  return (
    <div className="assistant">
      <h3>AI Assistant</h3>
      <textarea value={q} onChange={e=>setQ(e.target.value)} placeholder="Ask about detection, hotspots, or how to run experiments" />
      <button onClick={ask}>Ask</button>
      <div className="assistant-answer">{answer}</div>
    </div>
  );
}
