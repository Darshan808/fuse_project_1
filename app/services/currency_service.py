"""
Service for handling currency exchange operations.
"""

import json
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, Tuple

import httpx

from app.config import get_settings


class CurrencyService:
    """Service for fetching exchange rates and performing conversions."""

    def __init__(self, redis_client=None):
        """Initialize with optional Redis client for caching."""
        self.settings = get_settings()
        self.api_url = self.settings.EXCHANGE_API_URL
        self.api_key = self.settings.EXCHANGE_API_KEY
        self.redis_client = redis_client

    async def get_exchange_rates(self, base_currency: str = "USD") -> Tuple[Dict[str, float], str]:
        """
        Fetch current exchange rates from the API or cache.

        Args:
            base_currency: Base currency code (default: USD)

        Returns:
            Tuple of exchange rates dict and timestamp
        """
        cache_key = f"exchange_rates:{base_currency}"

        # Try to get from cache first
        if self.redis_client:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                data = json.loads(cached_data)
                return data["rates"], data["timestamp"]

        # Fetch from API if not cached
        async with httpx.AsyncClient() as client:
            params = {"base": base_currency}
            if self.api_key != "demo_key":
                params["apikey"] = self.api_key

            url = f"{self.api_url}/{self.api_key}/latest/{base_currency}"
            print(f"Hitting API: {url}")
            response = await client.get(url)

            if response.status_code != 200:
                raise Exception(f"API error: {response.text}")

            data = response.json()
            rates = data.get("conversion_rates", {})
            timestamp = data.get("time_last_update_utc", datetime.now().isoformat())

            # Store in cache if Redis is available
            if self.redis_client:
                cache_data = {"rates": rates, "timestamp": timestamp}
                self.redis_client.setex(cache_key, self.settings.CACHE_TTL, json.dumps(cache_data))

            return rates, timestamp

    async def convert_currency(self, from_currency: str, to_currency: str, amount: Decimal) -> Dict:
        """
        Convert an amount from one currency to another.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            amount: Amount to convert

        Returns:
            Dictionary with conversion details
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Get exchange rates
        rates, timestamp = await self.get_exchange_rates(from_currency)

        if to_currency not in rates:
            raise ValueError(f"Currency {to_currency} not found")

        exchange_rate = Decimal(str(rates[to_currency]))
        converted_amount = amount * exchange_rate

        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": converted_amount,
            "exchange_rate": exchange_rate,
            "timestamp": timestamp,
        }
