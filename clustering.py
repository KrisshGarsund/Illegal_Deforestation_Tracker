# backend/app/services/clustering.py
from typing import List, Tuple, Dict, Any
from detection import incident_bbox, incident_centroid

def build_incident_objects(cases: List[List[Tuple[int,int]]], t0_id: str, t1_id: str) -> List[Dict[str, Any]]:
    incidents: List[Dict[str, Any]] = []
    for k, cells in enumerate(cases, start=1):
        bbox = incident_bbox(cells)
        cx, cy = incident_centroid(cells)
        severity = len(cells)
        # Map grid centroid to a demo lat/lng for visualization (simple mapping)
        lat = 10 + (cx / max(1, bbox[2])) * 20
        lng = 70 + (cy / max(1, bbox[3] if bbox[3]>0 else 1)) * 20
        incidents.append({
            "case_id": f"C{k:04d}",
            "cells": cells,
            "severity": float(severity),
            "centroid": (lat, lng),
            "bbox": tuple(map(float, bbox)),
            "t0_id": t0_id,
            "t1_id": t1_id
        })
    return incidents
