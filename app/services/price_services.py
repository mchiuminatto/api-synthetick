import pandas as pd
from synthetick import synthetick
from app.models.currency_types import TimeFrame, InstrumentType, PriceSide
from app.common import constants as const
import abc
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PriceDataSetSpecification:
    symbol: str
    trend: float
    volatility_range: float
    spread_min: float
    spread_max: float
    remove_weekend: bool
    records: int
    instrument_type: InstrumentType
    frequency: TimeFrame
    pip_position: int
    price_side: PriceSide | None = None


# TODO: move this factory pattern to synthetick library in the future

class PriceGenerator(abc.ABC):

    @abc.abstractmethod
    async def produce(self, date_from: str, date_to: str, init_value: float):
        pass


class TickPriceDataSet(PriceGenerator):

    def __init__(self, specification: PriceDataSetSpecification):
        self.specification = specification

        self.ticks: synthetick.Ticks = synthetick.Ticks(
            trend=specification.trend,
            volatility_range=specification.volatility_range,
            spread_min=specification.spread_min,
            spread_max=specification.spread_max,
            pip_position=specification.pip_position,
            remove_weekend=specification.remove_weekend,
        )

    async def produce(self, date_from: datetime, date_to: datetime, init_value: float) -> pd.DataFrame:
        self.ticks.produce(date_from=date_from, date_to=date_to,
                           frequency=const.TICK_FREQUENCY,
                           init_value=init_value)
        return self.ticks.price_time_series


class OHLCPriceDataSet(PriceGenerator):

    def __init__(self, specification: PriceDataSetSpecification):
        self.specification = specification

        self.ohlc: synthetick.OHLC = synthetick.OHLC(
            trend=specification.trend,
            volatility_range=specification.volatility_range,
            spread_min=specification.spread_min,
            spread_max=specification.spread_max,
            pip_position=specification.pip_position,
            remove_weekend=specification.remove_weekend,
            tick_frequency=const.TICK_FREQUENCY,
            time_frame=specification.frequency
        )

    async def produce(self, date_from: datetime, date_to: datetime, init_value: float):
        self.ohlc.produce(date_from=date_from, date_to=date_to, init_value=init_value)
        return self.ohlc.ohlc_time_series[self.specification.price_side.value]


class PriceGeneratorFactory:

    @staticmethod
    def create_price_data_set(specification: PriceDataSetSpecification) -> PriceGenerator:
        if specification.frequency == TimeFrame.TICK:
            return TickPriceDataSet(specification)
        else:
            return OHLCPriceDataSet(specification)
class PriceProducerService:
    """ Service to produce price data sets based on specifications. """

    @staticmethod
    async def generate_price_data_set(specification: PriceDataSetSpecification,
                                      date_from: datetime,
                                      date_to: datetime,
                                      init_value: float) -> pd.DataFrame:



        generator = PriceGeneratorFactory().create_price_data_set(specification)
        return await generator.produce(date_from=date_from, date_to=date_to, init_value=init_value)

