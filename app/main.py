from datetime import datetime
from typing import Annotated
from string import digits, ascii_uppercase
import random

from fastapi import FastAPI, Query
from pydantic import BaseModel
from .currency_types import PriceDataRequest, CurrencyPair, TimeFrame
from . import constants as const


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Synthetic": f"version {const.VERSION}"}


@app.post("/forex/request/")
async def gen_price_by_start_date_and_records(
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
):
    """Generate synthetic data for a given currency code,
    starting from a specific date, and for a
    specified number of records."""
    

    return {
        "symbol": currency_code,
        "time_frame": time_frame,
        "start_date": start_date,
        "end-date": end_date,
        "records": records,
        "request_id": "".join(
            random.choice(digits + ascii_uppercase)
            for _ in range(const.REQUEST_ID_SIZE)
        ),
        "message": "Data generation is not implemented yet.",
    }


@app.get("/forex/status/")
def get_status(
    request_id: Annotated[
        str,
        Query(
            title="Request ID",
            description="The unique identifier for the request.",
            min_length=const.REQUEST_ID_SIZE,
            max_length=const.REQUEST_ID_SIZE,
        ),
    ],
):
    return {"status": "API is running",
            "records-generated": 0}


@app.get("/forex/data/")
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
