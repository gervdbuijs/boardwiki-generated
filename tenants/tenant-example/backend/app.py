"""
BoardWiki gegenereerde backend voor: tenant-example
Gegenereerd op: zie manifest.json
Stack: Python 3.12 + FastAPI + MongoDB Atlas
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
import os

# ── Configuratie ──────────────────────────────────────────
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME     = os.getenv("DB_NAME", "tenant_example")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# ── App initialisatie ─────────────────────────────────────
app = FastAPI(
    title="tenant-example API",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENV") != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Database connectie ────────────────────────────────────
@app.on_event("startup")
async def startup():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URI)
    app.db = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()

# ── Models ────────────────────────────────────────────────
class Item(BaseModel):
    name: str
    description: str | None = None

# ── Routes ────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "tenant": "tenant-example"}

@app.get("/items")
async def get_items():
    items = []
    async for item in app.db.items.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items

@app.post("/items", status_code=201)
async def create_item(item: Item):
    result = await app.db.items.insert_one(item.dict())
    return {"id": str(result.inserted_id), **item.dict()}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await app.db.items.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item niet gevonden")
    return {"deleted": item_id}

@app.get("/debug")
async def debug():
    return {
        "allowed_origins": ALLOWED_ORIGINS,
        "mongodb_uri_set": bool(MONGODB_URI),
    }