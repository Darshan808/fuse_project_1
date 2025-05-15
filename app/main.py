"""
Main FastAPI application module.
"""

import redis
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import ConversionRequest, ConversionResponse, ErrorResponse, ExchangeRatesResponse
from app.services import CurrencyService

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="A microservice for currency conversion",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis connection (if available)
redis_client = None
if settings.REDIS_HOST:
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
    except Exception as e:
        print(f"Redis connection error: {e}")


# Dependency to get the currency service
def get_currency_service():
    """Dependency to provide a configured CurrencyService instance."""
    return CurrencyService(redis_client=redis_client)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.APP_NAME}


@app.get("/rates/{base_currency}", response_model=ExchangeRatesResponse, tags=["Currency"])
async def get_exchange_rates(base_currency: str = "USD", service: CurrencyService = Depends(get_currency_service)):
    """
    Get the latest exchange rates for a base currency.

    Args:
        base_currency: Base currency code (default: USD)
    """
    try:
        rates, timestamp = await service.get_exchange_rates(base_currency)
        return {
            "base_currency": base_currency,
            "rates": rates,
            "timestamp": timestamp,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert", response_model=ConversionResponse, tags=["Currency"])
async def convert_currency(request: ConversionRequest, service: CurrencyService = Depends(get_currency_service)):
    """
    Convert an amount from one currency to another.

    Args:
        request: Conversion request with from_currency, to_currency, and amount
    """
    try:
        result = await service.convert_currency(
            request.from_currency,
            request.to_currency,
            request.amount,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
