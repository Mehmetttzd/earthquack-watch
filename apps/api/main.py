from fastapi import FastAPI, Query
import httpx
from datetime import datetime, timezone
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="QuakeWatch API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
USGS_FEEDS = {
    "hour": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
    "day": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
    "week": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson",
}

Window = Literal["hour", "day", "week"]


def iso_utc(ms: int | None) -> str | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/quakes")
async def quakes(
    window: Window = Query("day", description="Time window: hour/day/week"),
    minMag: float = Query(0.0, ge=0.0, description="Minimum magnitude filter"),
    limit: int = Query(50, ge=1, le=200, description="Max results returned"),
):
    url = USGS_FEEDS[window]

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()

    features = data.get("features", [])
    items = []

    for f in features:
        props = f.get("properties") or {}
        geom = f.get("geometry") or {}
        coords = (geom.get("coordinates") or [None, None, None])

        mag = props.get("mag")
        if mag is None or mag < minMag:
            continue

        items.append(
            {
                "id": f.get("id"),
                "mag": mag,
                "place": props.get("place"),
                "time": iso_utc(props.get("time")),
                "updated": iso_utc(props.get("updated")),
                "url": props.get("url"),
                "tsunami": props.get("tsunami"),
                "felt": props.get("felt"),
                "sig": props.get("sig"),
                "depth_km": coords[2],
                "longitude": coords[0],
                "latitude": coords[1],
            }
        )

    # Sort by most recent time (desc)
    items.sort(key=lambda x: x["time"] or "", reverse=True)

    return {
        "meta": {
            "source": "USGS",
            "window": window,
            "minMag": minMag,
            "count": len(items[:limit]),
            "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        },
        "items": items[:limit],
    }
