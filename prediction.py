# backend/app/services/prediction.py
from typing import List, Dict, Any
import numpy as np

def _make_features(incidents: List[Dict[str, Any]]) -> Any:
    X = []
    for inc in incidents:
        sev = inc.get("severity", 1.0)
        area = len(inc.get("cells", []))
        cx,cy = inc.get("centroid",[0.0,0.0])
        X.append([sev, area, cx, cy])
    return np.array(X) if X else np.empty((0,4))

def predict_hotspots(incidents: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    if not incidents:
        return []
    X = _make_features(incidents)
    # scoring heuristic
    scores = (X[:,0]*0.6 + X[:,1]*0.35 + (X[:,2]+X[:,3])*0.05)
    idx = list(reversed(sorted(range(len(scores)), key=lambda i: scores[i])))[:top_k]
    hotspots: List[Dict[str, Any]] = []
    for i in idx:
        inc = incidents[i]
        hotspots.append({"case_id": inc["case_id"], "score": float(scores[i]), "centroid": inc["centroid"]})
    return hotspots
