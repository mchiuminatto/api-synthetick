from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

from redis import Redis

from fastapi import APIRouter
from fastapi import Query, Path, Depends

from app.currency_types import CurrencyPair
import app.common.constants as const
from app.common.utils import gen_random_alfa
from app.common.mem_cache import mem_cache, MemCache

router = APIRouter()


def get_mem_cache() -> MemCache:
    return mem_cache


class PriceDatasetRequest(BaseModel):
    symbol: Annotated[CurrencyPair, Field(title="Symbol code")]
    start_date: Annotated[datetime, Field(title="Start date")]
    end_date: Annotated[datetime | None, Field(title="End date of the range. "
                                                     "Optional and ignored if 'records' > 0")] = None
    trend: Annotated[float | None, Field(title="Trend direction and strength. Positive for upward trend, "
                                               "negative for downward trend, zero for no trend")] = 0.0
    volatility: Annotated[float | None, Field(title="Volatility level. "
                                                    "Higher values indicate more price fluctuations", ge=0)] = 0.1
    spred_max: Annotated[float | None, Field(title="Maximum spread value", gt=0)] = 0.001
    spread_min: Annotated[float | None, Field(title="Minimum spread value", gt=0)] = 0.0001
    records: Annotated[int | None, Field(description="Number of records to produce", gt=0)] = 1000


@router.post("/request/")
def gen_price_by_start_date_and_records(
        price_data_request: PriceDatasetRequest,
        mem_cache_cli: Redis = Depends(get_mem_cache)
):
    """Generate synthetic data for a given currency code,
    starting from a specific date, and for a
    specified number of records."""

    # set session in memcache

    # TODO: use dependency injection 

    session_key = gen_random_alfa(const.REQUEST_ID_SIZE)

    mem_cache_cli.set(session_key, "status", "not-started")
    mem_cache_cli.set(session_key, "records-processed", 0)

    # trigger background task to generate data (not implemented)

    return {
        "symbol": price_data_request.symbol,
        "start_date": price_data_request.start_date,
        "end-date": price_data_request.end_date,
        "records": price_data_request.records,
        "spread_min": price_data_request.spread_min,
        "spred_max": price_data_request.spred_max,
        "volatility": price_data_request.volatility,
        "trend": price_data_request.trend,
        "request_id": session_key,
        "message": "Data generation is not implemented yet.",
    }


@router.get("/status/{request_id}")
def get_status(
        request_id: Annotated[
            str,
            Path(
                title="Request ID",
                description="The unique identifier for the request.",
                min_length=const.REQUEST_ID_SIZE,
                max_length=const.REQUEST_ID_SIZE,
            ),
        ],

        mem_cache_cli: MemCache = Depends(get_mem_cache)
):
    process_status = mem_cache_cli.get(request_id, "status")
    records_generated = mem_cache_cli.get(request_id, "records-processed")

    return {"status": process_status, "records-generated": records_generated}


@router.get("/data/")
def get_actual_data(
        request_id: Annotated[
            str,
            Query(
                title="Request ID",
                description="The unique identifier for the request.",
                min_length=const.REQUEST_ID_SIZE,
                max_length=const.REQUEST_ID_SIZE,
            ),
        ],
        start_date: Annotated[
            datetime | None,
            Query(
                title="Start Date",
                description="The start date for data retrieval in ISO format.",
            ),
        ],
        end_date: Annotated[
            datetime | None,
            Query(
                title="End Date",
                description="The end date for data retrieval in ISO format. Optional.",
            ),
        ] = None,
        records: Annotated[
            int | None,
            Query(
                title="Number of Records",
                description="The number of records to retrieve. Optional.",
            ),
        ] = None,
):
    return {
        "request_id": request_id,
        "start_date": start_date,
        "end-date": end_date,
        "records": records,
        "message": "Data retrieval is not implemented yet.",
    }
