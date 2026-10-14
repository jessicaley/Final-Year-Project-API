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
async def test_get_employee_success():
    mock_employee = [{
        "employee_id": 1,
        "job_scope": "Director",
        "address": "22 Libra Avenue, Sundowner, Johannesburg",
        "user_id": 1,
        "emergency_contact": "911",
        "hourly_rate": 89.99
    }]
    
    with patch('api.Data.supabase.get_employee_sb', return_value=mock_employee):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/employees/get_employee/1")

        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        print(f"Expected: {mock_employee}")
        
        assert response.status_code == 200
        assert response.json() == mock_employee

@pytest.mark.asyncio
async def test_get_employee_not_found():
    with patch('api.Data.supabase.get_employee_sb', return_value=[]):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/employees/get_employee/999")
        
        assert response.status_code == 200
        assert response.json() == []

# Test database error
@pytest.mark.asyncio
async def test_get_employee_database_error():
    # Mock exception
    with patch('api.Data.supabase.get_employee_sb', side_effect=Exception("DB Connection Failed")):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/employees/get_employee/1")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        print(f"Expected: {response}")

        assert response.status_code == 200
        assert "error" in response.json()