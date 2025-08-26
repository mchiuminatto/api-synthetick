from datetime import datetime

from enum import Enum
from pydantic import BaseModel

class CurrencyPair(str, Enum):
    EURUSD = "EURUSD"
    USDJPY = "USDJPY"
    GBPUSD = "GBPUSD"
    AUDUSD = "AUDUSD"
    USDCAD = "USDCAD"
    NZDUSD = "NZDUSD"
    AUDJPY = "AUDJPY"
    NZDJPY = "NZDJPY"
    GBPJPY = "GBPJPY"
    USDCHF = "USDCHF"
    CHFJPY = "CHFJPY"


class TimeFrame(str, Enum):
    M1 = "M1"  # 1 minute
    M5 = "M5"  # 5 minutes
    M15 = "M15"  # 15 minutes
    M30 = "M30"  # 30 minutes
    H1 = "H1"  # 1 hour
    H4 = "H4"  # 4 hours
    D1 = "D1"  # Daily
    W1 = "W1"  # Weekly
    MN = "MN"  # Monthly
    

class TredeDelta(float, Enum):
    FLAT = 0
    UP_WEAK = 0.1
    UP_STRONG = 1
    DOWN_STRONG = -1
    DOWN_WEAK = -0.1
    

class PriceDataRequest(BaseModel):
    currency_code: CurrencyPair
    time_frame: TimeFrame
    start_date: str  # ISO format date string
    end_date: str | None = None  # ISO format date string, optional
    records: int | None = 1000  # Optional, default to 1000
    trend: float | TredeDelta = 0.0  # Optional, default to 0.0
        
