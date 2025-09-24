# backend/app/services/ingestion.py

import json
from pathlib import Path
import random
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
TILES = DATA_DIR / "tiles.json"
INC = DATA_DIR / "incidents.json"

def _init_files() -> None:
    if not TILES.exists(): TILES.write_text("[]")
    if not INC.exists(): INC.write_text("[]")

def _load(p: Path) -> Any:
    return json.loads(p.read_text())

def _save(p: Path, data: Any) -> None:
    p.write_text(json.dumps(data, indent=2))

def store_tile(tile: Dict[str, Any]) -> None:
    tiles = _load(TILES)
    tiles = [t for t in tiles if t.get("tile_id") != tile["tile_id"]]
    tiles.append(tile)
    _save(TILES, tiles)

def get_tile(tile_id: str) -> Optional[Dict[str, Any]]:
    tiles = _load(TILES)
    for t in tiles:
        if t.get("tile_id") == tile_id:
            return t
    return None

def list_tiles() -> List[Dict[str, Any]]:
    return _load(TILES)

def store_incidents(incidents: List[Dict[str, Any]]) -> None:
    _save(INC, incidents)

def list_incidents() -> List[Dict[str, Any]]:
    return _load(INC)

# --- Synthetic NDVI-like generator ---
def synth_grid(n: int = 64, forest_base: float = 0.85, noise: float = 0.04) -> List[List[float]]:
    import random
    return [[max(0.0,min(1.0, random.gauss(forest_base, noise))) for _ in range(n)] for _ in range(n)]

def perturb_deforestation(grid: List[List[float]], drop: float = 0.35, patches: int = 4, patch_size: int = 6) -> List[List[float]]:
    import random
    n = len(grid)
    for _ in range(patches):
        x = random.randint(0, max(0, n-patch_size))
        y = random.randint(0, max(0, n-patch_size))
        for i in range(x, min(n, x+patch_size)):
            for j in range(y, min(n, y+patch_size)):
                grid[i][j] = max(0.0, grid[i][j] - drop)
    return grid

def create_synth_pair(n: int = 64, drop: float = 0.35) -> Dict[str, Any]:
    t0 = {"tile_id":"T0","bbox":(0.0,0.0,1.0,1.0),"timestamp":"2025-01-01T00:00:00Z","grid":synth_grid(n=n)}
    g1 = [row[:] for row in t0["grid"]]
    g1 = perturb_deforestation(g1, drop=drop, patches=5, patch_size=max(3, n//12))
    t1 = {"tile_id":"T1","bbox":(0.0,0.0,1.0,1.0),"timestamp":"2025-02-01T00:00:00Z","grid":g1}
    store_tile(t0); store_tile(t1)
    return {"ok": True, "tiles":[t0["tile_id"], t1["tile_id"]]}
