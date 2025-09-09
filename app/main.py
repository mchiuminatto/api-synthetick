
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from .currency_types import PriceDataRequest, CurrencyPair, TimeFrame
from . import constants as const
from app.api.endpoints import dataset


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Synthetic": f"version {const.VERSION}"}

# routers
app.include_router(dataset.router, prefix="/api/v1/forex", tags=["forex-dataset"])

# 
