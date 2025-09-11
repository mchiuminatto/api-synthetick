from datetime import datetime
from typing import Annotated

from redis import Redis

from fastapi import APIRouter
from fastapi import FastAPI, Query, Path, Depends

from app.currency_types import PriceDataRequest, CurrencyPair, TimeFrame
import app.constants as const
from app.utils import gen_random_alfa
from app.api.dependencies import pool


router = APIRouter()

def get_redis() -> Redis:
    return Redis(connection_pool=pool)


@router.post("/request/")
def gen_price_by_start_date_and_records(
        currency_code: Annotated[
        CurrencyPair,
        Query(
            title="Currency Code",
            description="The currency pair code, e.g., EURUSD, USDJPY.",
        ),
    ],
    time_frame: Annotated[
        TimeFrame,
        Query(
            title="Time Frame",
            description="The time frame for the data, e.g., M1, H1, D1.",
        ),
    ],
    start_date: Annotated[
        datetime,
        Query(
            title="Start Date",
            description="The start date for data generation in ISO format.",
        ),
    ],
    end_date: Annotated[
        datetime | None,
        Query(
            title="End Date",
            description="The end date for data generation in ISO format. Optional.",
        ),
    ] = None,
    records: Annotated[
        int | None,
        Query(
            title="Number of Records",
            description="The number of records to generate. Optional, default is 1000.",
        ),
    ] = 1000,
    redis_cli: Redis = Depends(get_redis)

):
    """Generate synthetic data for a given currency code,
    starting from a specific date, and for a
    specified number of records."""
    
    # set session in memcache
    
    # TODO: use dependency injection 
    
    session_key = gen_random_alfa(const.REQUEST_ID_SIZE)
    redis_cli.set(f"{session_key}:status", "not-started")
    redis_cli.set(f"{session_key}:records-processed", 0)
    
    # trigger background task to generate data (not implemented)

    return {
        "symbol": currency_code,
        "time_frame": time_frame,
        "start_date": start_date,
        "end-date": end_date,
        "records": records,
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

    redis_cli: Redis = Depends(get_redis)
):
    process_status = redis_cli.get(f"{request_id}:status")
    records_generated = redis_cli.get(f"{request_id}:records-processed")
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
