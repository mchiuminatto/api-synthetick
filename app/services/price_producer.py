"""
Synthetick wrapper module
"""

import abc
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from synthetick.synthetick import Ticks

from app.models.currency_types import TimeFrame, InstrumentType, PriceSide


@dataclass
class SynthetickPriceSpec:
    """
    Data class for synthetick historic price specification
    """

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
    date_from: datetime
    date_to: datetime
    price_side: PriceSide | None = None
    init_value: float = 0.0


class Synthetick(abc.ABC):
    """
    Abstract base class for synthetick data generators.
    """

    @abc.abstractmethod
    async def produce(self, price_spec: SynthetickPriceSpec):
        """
        Price producer method
        """
        ...


class SynthetickProducer(Synthetick):
    """
    Synthetick producer class (Facade)
    """

    async def produce(self, price_spec: SynthetickPriceSpec) -> pd.DataFrame:
        """
        Generate synthetic data asynchronously
        """
        pass


class HistoricPriceGenerator(abc.ABC):
    """
    Abstract base class for historic price generators.
    """

    @abc.abstractmethod
    async def produce(self) -> pd.DataFrame:
        pass


class TickPriceGenerator(HistoricPriceGenerator):
    """
    Tick price generator class
    """
    def __init__(self, specification: SynthetickPriceSpec):
        self.__spec = specification

        self.ticks: Ticks = Ticks(
            trend=specification.trend,
            volatility_range=specification.volatility_range,
            spread_min=specification.spread_min,
            spread_max=specification.spread_max,
            pip_position=specification.pip_position,
            remove_weekend=specification.remove_weekend
        )

    async def produce(self) -> pd.DataFrame:
        self.ticks.produce(date_from=self.__spec.date_from,
                           date_to=self.__spec.date_to,
                           frequency=self.__spec.frequency,
                           init_value=self.__spec.init_value)

        return self.ticks.price_time_series
