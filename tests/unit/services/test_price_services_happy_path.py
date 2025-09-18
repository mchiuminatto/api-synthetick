from app.services.date_range_calculations import PeriodsCalculator
from app.services.price_services import PriceGenerator
"""
Strategy to produce price

Generate chunks of reduced size and then store them on the database
asynchronously

"""


class TestPeriodsCalculations:

    def test_periods_calculation_intraday_h1(self):
        """ Test the calculation of periods between two dates
        including weekends

        """

        period_calc = PeriodsCalculator()
        assert periods_calc.compute("2025-01-01 00:00:00", "2025-01-02 00:00:00", "H1") == 24

    def test_periods_calculation_intraday_h4(self):
        """ Test the calculation of periods between two dates
        including weekends

        """

        period_calc = PeriodsCalculator()
        assert periods_calc.compute("2025-01-01 00:00:00", "2025-01-02 00:00:00", "H4") == 6


    def test_periods_calculation_h4_no_weekend(self):
        """ Test the calculation of periods between two dates
        including weekends

        """

        period_calc = PeriodsCalculator()
        assert periods_calc.compute("2025-01-01 00:00:00", "2025-01-03 00:00:00", "H4") == 12



    def test_periods_calculation_h4_weekend(self):
        """ Test the calculation of periods between two dates
        including weekends

        """

        period_calc = PeriodsCalculator()
        assert periods_calc.compute("2025-01-03 00:00:00", "2025-01-06 00:00:00", "H4") == 0

    def test_price_generator_one_chunk(self):
        pass


