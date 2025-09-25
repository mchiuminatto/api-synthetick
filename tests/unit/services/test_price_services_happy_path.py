from app.services.price_services import PriceGenerator
from app.currency_types import Trend, TimeFrame, InstrumentType, PriceSide


class TestPriceGeneration:
    def test_generate_tick_small_range(self):
        generator: PriceGenerator = PriceGenerator(trend=Trend.FLAT,
                                                   volatility_range=0.01,
                                                   spread_min=0.1,
                                                   spread_max=1,
                                                   remove_weekend=False,
                                                   instrument_type=InstrumentType.FOREX,
                                                   frequency=TimeFrame.TICK
                                                   )
        data_set = generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-01-02 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == "2023-01-01 00:00:00"
        assert data_set.index[-1] == "2023-01-02 00:00:00"
        assert data_set["ask"]-data_set["bid"].min() >= 0.1
        assert data_set["ask"]-data_set["bid"].max() <= 1


    def test_generate_tick_large_range(self):
        generator: PriceGenerator = PriceGenerator(trend=Trend.FLAT,
                                                   volatility_range=0.01,
                                                   spread_min=0.1,
                                                   spread_max=1,
                                                   remove_weekend=False,
                                                   instrument_type=InstrumentType,
                                                   frequency=TimeFrame.TICK
                                                   )
        data_set = generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-02-01 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == "2023-01-01 00:00:00"
        assert data_set.index[-1] == "2023-02-01 00:00:00"
        assert data_set["ask"] - data_set["bid"].min() >= 0.1
        assert data_set["ask"] - data_set["bid"].max() <= 1

    def test_generate_ohlc_small_range(self):
        generator: PriceGenerator = PriceGenerator(trend=Trend.FLAT,
                                                   volatility_range=0.01,
                                                   spread_min=0.1,
                                                   spread_max=1,
                                                   remove_weekend=False,
                                                   instrument_type=InstrumentType,
                                                   frequency=TimeFrame.H1,
                                                   price_side=PriceSide.BID
                                                   )
        data_set = generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-01-02 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == "2023-01-01 00:00:00"
        assert data_set.index[-1] == "2023-01-02 00:00:00"
        assert data_set.columns.to_list() == ["open", "high", "low", "close"]


    def test_generate_ohlc_large_range(self):
        generator: PriceGenerator = PriceGenerator(trend=Trend.FLAT,
                                                   volatility_range=0.01,
                                                   spread_min=0.1,
                                                   spread_max=1,
                                                   remove_weekend=False,
                                                   instrument_type=InstrumentType,
                                                   frequency=TimeFrame.H1,
                                                   price_side=PriceSide.BID

                                                   )
        data_set = generator.produce(date_from="2023-01-01 00:00:00", date_to="2023-01-02 00:00:00", init_value=1.300)

        assert data_set is not None
        assert data_set.index[0] == "2023-01-01 00:00:00"
        assert data_set.index[-1] == "2023-01-02 00:00:00"
        assert data_set.columns.to_list() == ["open", "high", "low", "close"]


