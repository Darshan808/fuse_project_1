"""
Tests for the currency converter API.
"""

from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.currency_service import CurrencyService

# Create a test client
client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint for health check."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_get_exchange_rates():
    """Test getting exchange rates."""
    # Mock the currency service
    with patch.object(CurrencyService, "get_exchange_rates", new_callable=AsyncMock) as mock_get_rates:
        # Set up the mock return value
        mock_get_rates.return_value = ({"EUR": 0.85, "GBP": 0.75, "JPY": 110.0}, "2024-01-01 12:00:00")

        # Make the request
        response = client.get("/rates/USD")

        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["base_currency"] == "USD"
        assert "EUR" in data["rates"]
        assert data["rates"]["EUR"] == 0.85

        # Verify the mock was called
        mock_get_rates.assert_called_once_with("USD")


@pytest.mark.asyncio
async def test_convert_currency():
    """Test currency conversion."""
    # Mock the currency service
    with patch.object(CurrencyService, "convert_currency", new_callable=AsyncMock) as mock_convert:
        # Set up the mock return value
        mock_convert.return_value = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": Decimal("100"),
            "converted_amount": Decimal("85"),
            "exchange_rate": Decimal("0.85"),
            "timestamp": "2024-01-01 12:00:00",
        }

        # Make the request
        response = client.post("/convert", json={"from_currency": "USD", "to_currency": "EUR", "amount": 100})

        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["from_currency"] == "USD"
        assert data["to_currency"] == "EUR"
        assert data["amount"] == 100
        assert data["converted_amount"] == 85
        assert data["exchange_rate"] == 0.85

        # Verify the mock was called with correct args
        mock_convert.assert_called_once()
        args = mock_convert.call_args[0]
        assert args[0] == "USD"
        assert args[1] == "EUR"
        assert args[2] == Decimal("100")


@pytest.mark.asyncio
async def test_invalid_currency():
    """Test error handling for invalid currency."""
    # Mock the currency service to raise an error
    with patch.object(CurrencyService, "convert_currency", new_callable=AsyncMock) as mock_convert:
        # Set up the mock to raise an exception
        mock_convert.side_effect = ValueError("Currency XYZ not found")

        # Make the request with invalid currency
        response = client.post(
            "/convert", json={"from_currency": "USD", "to_currency": "XYZ", "amount": 100}  # Invalid currency
        )

        # Check response is an error
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]
