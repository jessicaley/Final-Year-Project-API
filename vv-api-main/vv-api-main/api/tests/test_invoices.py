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
async def test_get_stock_success():
    mock_stock = [{'stock_id': 1,
                   'created_at': '2025-05-19T14:10:52.184424+00:00',
                   'stock_details': {'name': 'Mahogany Plank',
                                     'price': 500,
                                     'material': {'material_id': 1,
                                                  'material_name': 'Mahogany Wood'},
                                     'stock_id': 1,
                                     'created_at': '2025-05-19T14:10:52.184424+00:00',
                                     'stock_type': {'type_name': 'Raw Timber',
                                                    'stock_type_id': 1},
                                     'description': 'High-quality mahogany wood plank for pattern making',
                                     'stock_level': 50,
                                     'stock_price': 100,
                                     'stock_category': {'category_name': 'Raw Materials and Patterns\n',
                                                        'stock_category_id': 1}}}]
    
    with patch('api.Data.supabase.get_stock_sb', return_value=mock_stock):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/stock/get_stock/1")

        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        print(f"Expected: {mock_stock}")
        
        assert response.status_code == 200
        assert response.json() == mock_stock

@pytest.mark.asyncio
async def test_get_stock_not_found():
    with patch('api.Data.supabase.get_stock_sb', return_value=[]):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/stock/get_stock/999")
        
        assert response.status_code == 200
        assert response.json() == []