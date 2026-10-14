import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

with patch.dict('os.environ', {
    'SUPA_URL': 'https://trkedwmdellrzzjbuvtr.supabase.co',
    'SUPA_ANON_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRya2Vkd21kZWxscnp6amJ1dnRyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYxMjUwNTQsImV4cCI6MjA2MTcwMTA1NH0.fWUwndN9Wy0sYGkkFOudEdcNa4yPxYiBtXGsPSqCu4k',
    'SUPA_SERVICE_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRya2Vkd21kZWxscnp6amJ1dnRyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjEyNTA1NCwiZXhwIjoyMDYxNzAxMDU0fQ.U2cf1V2MlyBGfNn6PSSb_354Bv9tixQR4VZmU4Lsaw0',
    'SUPA_SCHEMA': 'development'
}):
    from main import app

@pytest.mark.asyncio
async def test_get_user_success():
    mock_user = [{
        "user_id": 1,
        'created_at': '2025-05-17T08:17:35.58988+00:00',
        "role_id": 1,
        "title_id": 1,
        "name": "Krishna",
        "surname": "Moodley",
        "email_address": "krishnamoodley77@gmail.com",
        "phone_number": "27614639706",
        "image": "https://trkedwmdellrzzjbuvtr.supabase.co/storage/v1/object/public/images/1754849240547.jpg",
        "uuid": "d1952d0b-80d0-47f8-816f-dfce57e43d1f",
        "is_employee": True,
    }]
    
    with patch('api.Data.supabase.get_user_sb', return_value=mock_user):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/users/get_user/1")

        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        print(f"Expected: {mock_user}")
        
        assert response.status_code == 200
        assert response.json() == mock_user

@pytest.mark.asyncio
async def test_get_user_not_found():
    with patch('api.Data.supabase.get_user_sb', return_value=[]):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/users/get_user/999")
        
        assert response.status_code == 200
        assert response.json() == []