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
async def test_get_customer_success():
    mock_customer = [{
        "customer_id": 1,
        'created_at': '2025-05-01T09:00:00+00:00',
        "user_id": 7,
        "customer_type_id": 1,
        "address": "123 Main St, Pretoria",
        "company_name": "HRC Holdings (PTY) LTD",
        "registration_number": "2005/05/14/15454",
        "vat_number": "4001514547",
        "telephone": "0114251345"
    }]
    
    with patch('api.Data.supabase.get_customer_sb', return_value=mock_customer):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/customers/get_customer/1")

        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        print(f"Expected: {mock_customer}")
        
        assert response.status_code == 200
        assert response.json() == mock_customer

@pytest.mark.asyncio
async def test_get_customer_not_found():
    with patch('api.Data.supabase.get_customer_sb', return_value=[]):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/customers/get_customer/999")
        
        assert response.status_code == 200
        assert response.json() == []