from datetime import datetime
from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field


class PriceSide(str, Enum):
    BID = "bid"
    ASK = "ask"

class InstrumentType(str, Enum):
    FOREX = "forex"
    STOCK = "stock"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    ETF = "etf"
    INDEX = "index"

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
    TICK = "1S"  # Tick data
    M1 = "1M"  # 1 minute
    M5 = "5M"  # 5 minutes
    M15 = "15M"  # 15 minutes
    M30 = "30M"  # 30 minutes
    H1 = "1H"  # 1 hour
    H4 = "4H"  # 4 hours
    D1 = "1D"  # Daily
    W1 = "1W"  # Weekly
    MN = "MN"  # Monthly


class Trend(float, Enum):
    FLAT = 0
    UP_WEAK = 0.1
    UP_STRONG = 1
    DOWN_STRONG = -1
    DOWN_WEAK = -0.1


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
