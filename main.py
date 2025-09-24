# backend/app/main.py
from fastapi import FastAPI, Depends
from typing import Any
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import ingestion, detection, clustering, routing, prediction, assistant_service
from jwt_auth import get_current_user, create_access_token, authenticate_user, get_password_hash, fake_users_db
from schemas import TileIn, DetectRequest, RouteRequest, RouteResult, RangeStatRequest, UserCreate, Token


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    ingestion._init_files()
    yield

app = FastAPI(title="Illegal Deforestation Tracker", lifespan=lifespan)

# Allow frontend dev origin; restrict in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://127.0.0.1:8001", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# --- Auth endpoints (simple JWT flow) ---
@app.post("/api/register", response_model=Token)
def register(u: UserCreate) -> dict[str, Any]:
    if u.username in fake_users_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="User exists")
    fake_users_db[u.username] = {"username": u.username, "full_name": u.full_name, "hashed_password": get_password_hash(u.password), "role": "user"}
    token = create_access_token({"sub": u.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/token", response_model=Token)
def login(u: UserCreate) -> dict[str, Any]:
    user = authenticate_user(u.username, u.password)
    from fastapi import HTTPException
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# --- Tiles / ingestion ---
@app.post("/api/tiles")
def upload_tile(tile: TileIn, current: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    ingestion.store_tile(tile.model_dump())
    return {"ok": True, "tile_id": tile.tile_id}

@app.post("/api/synth-tiles")
def synth_tiles(n: int = 64, drop: float = 0.35, current: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    return ingestion.create_synth_pair(n=n, drop=drop)

# --- Detection & clustering ---
@app.post("/api/detect")
def detect(req: DetectRequest, current: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    t0 = ingestion.get_tile(req.t0_id)
    t1 = ingestion.get_tile(req.t1_id)
    from fastapi import HTTPException
    if not t0 or not t1:
        raise HTTPException(status_code=404, detail="Tiles missing")
    loss, mask = detection.detect_changes(t0["grid"], t1["grid"], req.loss_threshold)
    cases = detection.cluster_incidents(mask)
    incidents = clustering.build_incident_objects(cases, req.t0_id, req.t1_id)
    incidents = sorted(incidents, key=lambda x: -x["severity"])
    ingestion.store_incidents(incidents)
    hotspots = prediction.predict_hotspots(incidents)
    return {"n_cases": len(incidents), "incidents": incidents, "hotspots": hotspots}

@app.get("/api/incidents")
def list_incidents(current: dict[str, Any] = Depends(get_current_user)) -> list[Any]:
    return ingestion.list_incidents()

# --- Routing example ---
@app.post("/api/route", response_model=RouteResult)
def build_route(req: RouteRequest, current: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    pts = [tuple(req.start)] + [tuple(g) for g in req.goals]
    dist, path = routing.route(pts, tuple(req.start), tuple(req.goals[0]))
    return {"path": path, "distance": dist}

# --- Range stats (segment tree demo) ---
@app.post("/api/range-stats")
def range_stats(req: RangeStatRequest, current: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    return {"answers": detection.range_stats(req.values, req.queries)}

# --- Assistant ---
@app.post("/api/assistant")
def assistant(q: dict[str, Any], current: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    return assistant_service.handle_assistant(q.get("question", ""))

# Serve built React app from backend in production (place build in backend/frontend/build)
# The frontend build should be copied to backend/frontend/build (see README/run steps).
try:
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")
except Exception:
    # if frontend build not present, root will not serve static — still okay for dev
    pass

# FastAPI dependency import (placed at bottom to avoid circular import issues)
from fastapi import Depends
