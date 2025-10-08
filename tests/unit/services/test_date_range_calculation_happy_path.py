from app.services.date_range_calculations import TimeSeriesSizeCalculatorFactory, TimeSeriesType
from app.services.currency_types import TimeFrame
from datetime import datetime


class TestPeriodsCalculations:

    def test_periods_calculation_intraday_h1(self):
        """ Test the calculation of periods between two dates
        including weekends

        """

        period_calc = TimeSeriesSizeCalculatorFactory().create_time_series_calculator(
            time_series_type=TimeSeriesType.REGULAR,
            frequency=TimeFrame.H1,
            include_weekends=True
        )
        assert period_calc.compute(datetime.strptime("2025-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                                   datetime.strptime("2025-01-01 23:59:59", "%Y-%m-%d %H:%M:%S")) == 24

    def test_periods_calculation_intraday_h4(self):
        """ Test the calculation of periods between two dates
        including weekends

        """

        period_calc = TimeSeriesSizeCalculatorFactory().create_time_series_calculator(
            time_series_type=TimeSeriesType.REGULAR,
            frequency=TimeFrame.H4,
            include_weekends=True
        )

        assert period_calc.compute(datetime.strptime("2025-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                                   datetime.strptime("2025-01-01 23:59:59", "%Y-%m-%d %H:%M:%S")) == 6

    def test_periods_calculation_h4_weekday(self):
        """ Test the calculation of periods between two dates
        including weekends

        """

        period_calc = TimeSeriesSizeCalculatorFactory().create_time_series_calculator(
            time_series_type=TimeSeriesType.REGULAR,
            frequency=TimeFrame.H4,
            include_weekends=True
        )
        assert period_calc.compute(datetime.strptime("2025-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                                   datetime.strptime("2025-01-02 23:59:59", "%Y-%m-%d %H:%M:%S")) == 12



    
