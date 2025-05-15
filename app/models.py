"""
Pydantic models for request and response validation.
"""

from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel, Field, validator


class ConversionRequest(BaseModel):
    """Request model for currency conversion."""

    from_currency: str = Field(..., min_length=3, max_length=3, description="Source currency code (e.g., USD)")
    to_currency: str = Field(..., min_length=3, max_length=3, description="Target currency code (e.g., EUR)")
    amount: Decimal = Field(..., gt=0, description="Amount to convert")

    @validator("from_currency", "to_currency")
    def validate_currency_code(cls, v):
        """Ensure currency codes are uppercase."""
        return v.upper()


class ConversionResponse(BaseModel):
    """Response model for currency conversion."""

    from_currency: str
    to_currency: str
    amount: Decimal
    converted_amount: Decimal
    exchange_rate: Decimal
    timestamp: str


class ExchangeRatesResponse(BaseModel):
    """Response model for retrieving exchange rates."""

    base_currency: str
    rates: Dict[str, float]
    timestamp: str


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str
    detail: Optional[str] = None
