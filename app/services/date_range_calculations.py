from datetime import datetime
import pandas as pd
import abc
import enum
from app.currency_types import TimeFrame


class TimeSeriesType(str, enum.Enum):
    REGULAR = "regular"
    NON_REGULAR = "non-regular"


class TimeSeriesSizeCalculator(abc.ABC):

    @abc.abstractmethod
    def compute(self, start_date: datetime, end_date: datetime) -> int:
        pass


class TimeSeriesSizeCalculatorFactory:

    def __init__(self):
        self.__registry: dict = {TimeSeriesType.REGULAR: RegularTimeSeries}

    @staticmethod
    def create_time_series_calculator(time_series_type: TimeSeriesType, **kwargs) -> TimeSeriesSizeCalculator:
        if time_series_type == TimeSeriesType.REGULAR:
            return RegularTimeSeries(frequency=kwargs["frequency"].value,
                                     include_weekends=kwargs["include_weekends"])
        elif time_series_type == TimeSeriesType.NON_REGULAR:
            raise TypeError("NON-REGULAR note supported yet")
        raise ValueError(f"Not supported time series types. {TimeSeriesType.value}")


class RegularTimeSeries(TimeSeriesSizeCalculator):

    def __init__(self, frequency: str, include_weekends: bool):
        self.frequency: str = frequency
        self.include_weekends: bool = include_weekends

    def compute(self, start_date: datetime, end_date: datetime):

        date_index = pd.date_range(start_date, end_date, freq=self.frequency)
        if not self.include_weekends:
            mask = date_index.day_of_week < 5
            return len(date_index[mask])
        return len(date_index)
