import asyncio
import pytest
from app.services.price_services import PriceDaSetSpecification, PriceGeneratorFactory
from app.currency_types import Trend, TimeFrame, InstrumentType, PriceSide
from datetime import datetime


class TestPriceGeneration:

    @pytest.mark.asyncio
    async def test_generate_tick_small_range(self):
        price_spec: PriceDaSetSpecification = PriceDaSetSpecification(
            symbol="EURUSD",
            trend=Trend.FLAT,
            volatility_range=0.01,
            spread_min=1,
            spread_max=2,
            remove_weekend=False,
            records=0,
            instrument_type=InstrumentType.FOREX,
            frequency=TimeFrame.TICK,
            pip_position=-4
        )
        generator = PriceGeneratorFactory().create_price_data_set(price_spec)
        data_set = await generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-01-02 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == datetime.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert data_set.index[-1] == datetime.strptime("2023-01-02 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert float((data_set["ask"] - data_set["bid"]).round(4).min()) >= .0001
        assert float((data_set["ask"] - data_set["bid"]).round(4).max()) <= .0002

    @pytest.mark.asyncio
    async def test_generate_tick_large_range(self):
        price_spec: PriceDaSetSpecification = PriceDaSetSpecification(
            symbol="EURUSD",
            trend=Trend.FLAT,
            volatility_range=0.01,
            spread_min=1,
            spread_max=2,
            remove_weekend=False,
            records=0,
            instrument_type=InstrumentType.FOREX,
            frequency=TimeFrame.TICK,
            pip_position=-4
        )
        generator = PriceGeneratorFactory().create_price_data_set(price_spec)
        data_set = await generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-01-10 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == datetime.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert data_set.index[-1] == datetime.strptime("2023-01-10 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert float((data_set["ask"] - data_set["bid"]).round(4).min()) >= .0001
        assert float((data_set["ask"] - data_set["bid"]).round(4).max()) <= .0002

    @pytest.mark.asyncio
    async def test_generate_ohlc_small_range(self):
        price_spec: PriceDaSetSpecification = PriceDaSetSpecification(
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
            price_side=PriceSide.BID
        )
        generator = PriceGeneratorFactory().create_price_data_set(price_spec)
        data_set = await generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-01-02 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == datetime.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert data_set.index[-1] == datetime.strptime("2023-01-02 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert data_set.columns.to_list() == ["open", "high", "low", "close"]

    @pytest.mark.asyncio
    async def test_generate_ohlc_large_range(self):
        price_spec: PriceDaSetSpecification = PriceDaSetSpecification(
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
            price_side=PriceSide.BID
        )
        generator = PriceGeneratorFactory().create_price_data_set(price_spec)
        data_set = await generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-05-01 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == datetime.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert data_set.index[-1] == datetime.strptime("2023-05-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert data_set.columns.to_list() == ["open", "high", "low", "close"]
