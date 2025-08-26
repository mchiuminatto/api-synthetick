from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from .currency_types import PriceDataRequest



app = FastAPI()

@app.get("/")
async def read_root():
    return {"Synthetic": "version 0.0.1"}


@app.post("/forex/dataset/")
async def gen_price_by_start_date_and_records(
                                                dataset_spec: PriceDataRequest
                                            ):
    """Generate synthetic data for a given currency code, 
    starting from a specific date, and for a 
    specified number of records."""
    
    return {"currency_code": dataset_spec.currency_code,
            "time_frame": dataset_spec.time_frame,
            "start_date": dataset_spec.start_date,
            "end-date": dataset_spec.end_date,
            "records": dataset_spec.records,
            "message": "Data generation is not implemented yet."}
    
    
    
    

    