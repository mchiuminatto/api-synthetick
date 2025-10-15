from datetime import datetime
import asyncio
import pytest 

import pandas as pd

from app.services.price_producer import SynthetickPriceSpec
from app.models.currency_types import InstrumentType, TimeFrame, Trend
from app.services.price_producer import SynthetickProducer


class TestSythetickFactory:

    @pytest.mark.asyncio
    async def test_tick_generator_creation(self):
        price_spec: SynthetickPriceSpec = SynthetickPriceSpec(
            symbol="EURUSD",
            trend=Trend.FLAT,
            volatility_range=0.01,
            spread_min=1,
            spread_max=2,
            remove_weekend=False,
            records=0,
            instrument_type=InstrumentType.FOREX,
            frequency=TimeFrame.TICK,
            pip_position=-4,
            date_from=datetime(2025, 1, 1),
            date_to=datetime(2025, 1, 3)
        )
        
        producer = SynthetickProducer()
        
        price_dataset: pd.DataFrame = await producer.produce(price_spec=price_spec)
        assert not price_dataset.empty
        assert list(price_dataset.columns) == ['timestamp', 'bid', 'ask']
        assert price_dataset['timestamp'].dtype == 'datetime64[ns]'

    @pytest.mark.asyncio
    async def test_ohlc_generator_creation(self):
        price_spec: SynthetickPriceSpec = SynthetickPriceSpec(
            symbol="EURUSD",
            trend=Trend.FLAT,
            volatility_range=0.01,
            spread_min=1,
            spread_max=2,
            remove_weekend=False,
            records=0,
            instrument_type=InstrumentType.FOREX,
            frequency=TimeFrame.H1,
            pip_position=-4,
            date_from=datetime(2025, 1, 1),
            date_to=datetime(2025, 1, 3)
        )
        
        producer = SynthetickProducer()
        
        price_dataset: pd.DataFrame = await producer.produce(price_spec=price_spec)
        assert not price_dataset.empty
        assert list(price_dataset.columns) == ['timestamp', 'bid', 'ask']
        assert price_dataset['timestamp'].dtype == 'datetime64[ns]'