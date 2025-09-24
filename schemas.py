# backend/app/models/schemas.py
from pydantic import BaseModel
from typing import List, Tuple

class TileIn(BaseModel):
    tile_id: str
    bbox: Tuple[float,float,float,float]
    timestamp: str
    grid: List[List[float]]

class DetectRequest(BaseModel):
    t0_id: str
    t1_id: str
    loss_threshold: float = 0.25

class Incident(BaseModel):
    case_id: str
    cells: List[Tuple[int,int]]
    severity: float
    centroid: Tuple[float,float]
    bbox: Tuple[float,float,float,float]
    t0_id: str
    t1_id: str

class RouteRequest(BaseModel):
    start: Tuple[float,float]
    goals: List[Tuple[float,float]]

class RouteResult(BaseModel):
    path: List[int]
    distance: float

class RangeStatRequest(BaseModel):
    values: List[float]
    queries: List[Tuple[int,int]]

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str = "User"

class Token(BaseModel):
    access_token: str
    token_type: str
