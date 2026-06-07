"""Basis tests voor tenant-example backend."""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from app import app


@pytest.fixture
def mock_db():
    """Mock MongoDB zodat tests zonder echte database draaien."""
    mock = MagicMock()
    mock.items.find.return_value.__aiter__ = AsyncMock(return_value=iter([]))
    mock.items.insert_one = AsyncMock(return_value=MagicMock(inserted_id="507f1f77bcf86cd799439011"))
    mock.items.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))
    return mock


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_get_items_empty(mock_db):
    app.db = mock_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_item(mock_db):
    app.db = mock_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "Test item", "description": "Test"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test item"
