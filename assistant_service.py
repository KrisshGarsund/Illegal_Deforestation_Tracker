# backend/app/services/assistant_service.py

import os, random
from typing import Dict, Any
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")

def handle_assistant(message: str) -> Dict[str, Any]:
    if not message:
        return {"reply": "Please ask a question about the project or incidents."}
    if OPENAI_KEY:
        # Proxy to OpenAI (user must set OPENAI_API_KEY). This is a best-effort example.
        import requests, json
        headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type":"application/json"}
        payload = {"model":"gpt-4o-mini","messages":[{"role":"user","content": message}], "max_tokens":300}
        try:
            r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
            j = r.json()
            content = j.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"reply": content or "No response from model."}
        except Exception as e:
            return {"reply": f"Error contacting OpenAI: {e}"}
    # fallback
    q = message.lower()
    if "hotspot" in q or "predict" in q:
        return {"reply": "Hotspot prediction is a scoring heuristic over incident severity and area. Run detection first."}
    if "how" in q and "run" in q:
        return {"reply": "Start backend and frontend servers. Or build frontend and serve via backend to run on one port."}
    return {"reply": random.choice(["I can help with detection, routing, and prediction. Try asking 'How to run detection?'","Ask me to synthesize tiles or explain the DSA parts."])}
