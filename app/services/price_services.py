import asyncio
from synthetick import synthetick
from app.currency_types import Trend, TimeFrame, InstrumentType, PriceSide
from app.common import constants as const
import abc


class PriceDaSetSpecification:
    def __init__(self,
                 symbol: str,
                 start_date: str,
                 end_date: str | None = None,
                 trend: float | None = 0.0,
                 volatility_range: float | None = 0.01,
                 spread_min: float = 0.1,
                 spread_max: float = 1.0,
                 remove_weekend: bool = True,
                 records: int | None = 0,
                 instrument_type: InstrumentType = InstrumentType.FOREX,
                 frequency: TimeFrame = TimeFrame.M1,
                 price_side: PriceSide = PriceSide.BID
                 ):
        self.symbol: str = symbol
        self.start_date: str = start_date
        self.end_date: str | None = end_date
        self.trend: float | None = trend
        self.volatility_range: float | None = volatility_range

        self.spread_min: float = spread_min
        self.spread_max: float = spread_max

        self.remove_weekend: bool = remove_weekend
        self.records: int | None = records
        self.instrument_type: InstrumentType = instrument_type
        self.frequency: TimeFrame = frequency
        self.price_side: PriceSide = price_side


# TODO: move thos factory pattern to synthetick library in the future

class PriceDataSet(abc.ABC):

    @abc.abstractmethod
    def produce(self, date_from: str, date_to: str, init_value: float):
        pass


class TickPriceDataSet(PriceDataSet):

    def __init__(self, specification: PriceDaSetSpecification):
        self.specification = specification

        self.ticks: synthetick.Ticks = synthetick.Ticks(trend=specification.trend,
                                                        volatility_range=specification.volatility_range,
                                                        spread_range=[specification.spread_min, specification.spread_max],
                                                        pip_position=specification.pip_position,
                                                        remove_weekend=specification.remove_weekend,
                                                        )

    def produce(self, date_from: str, date_to: str, init_value: float):
        self.ticks.produce(date_from=date_from, date_to=date_to, init_value=init_value)
        return self.ticks.ticks_time_series


class PriceDataSetFactory:

    @staticmethod
    def create_price_data_set(specification: PriceDaSetSpecification) -> PriceDataSet:
        if specification.frequency == TimeFrame.TICK:
            return synthetick.Ticks(ternd=specification.trend,
                                    volatility_range=specification.volatility_range,
                                    spread_min=specification.spread_min,
                                    spread_max=specification.spread_max,
                                    remove_weekend=specification.remove_weekend,
                                    instrument_type=specification.instrument_type.value,
                                    )
        else:
            return OHLCPriceDataSet(specification)


class PriceGenerator:

    def __init__(self,
                 dataset_specification: PriceDaSetSpecification
                 ):
        self.specification: PriceDaSetSpecification = dataset_specification
        self.tick_frequency = const.TICK_FREQUENCY
        self.price_generator: synthetick.PriceGenerator = synthetick.PriceGenerator(
            trend=self.specification.trend,
            volatility_range=self.specification.volatility_range,
            spread_min=self.specification.spread_min,
            spread_max=self.specification.spread_max,
            remove_weekend=self.specification.remove_weekend,
            instrument_type=self.specification.instrument_type.value,
            frequency=self.specification.frequency.value,
            price_side=self.specification.price_side.value
        ))
