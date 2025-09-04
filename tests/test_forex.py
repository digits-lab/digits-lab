import unittest
from app.services.forex import ForexService

class TestForexService(unittest.TestCase):

    def setUp(self):
        self.forex_service = ForexService()

    def test_get_rates_default_base(self):
        """Test getting rates with the default base currency (USD)."""
        rates = self.forex_service.get_rates()
        self.assertIn("USD", rates)
        self.assertAlmostEqual(rates["USD"], 1.0)
        self.assertIn("KES", rates)
        self.assertAlmostEqual(rates["KES"], 130.5)

    def test_get_rates_custom_base(self):
        """Test getting rates with a custom base currency (EUR)."""
        rates = self.forex_service.get_rates("EUR")
        self.assertIn("EUR", rates)
        self.assertAlmostEqual(rates["EUR"], 1.0)
        # USD rate should be 1 / 0.92 = 1.0869...
        self.assertAlmostEqual(rates["USD"], 1 / 0.92)

    def test_convert(self):
        """Test currency conversion."""
        # Convert 100 USD to KES
        converted_amount = self.forex_service.convert("USD", "KES", 100)
        self.assertAlmostEqual(converted_amount, 13050.0)

        # Convert 100 EUR to USD
        converted_amount_eur = self.forex_service.convert("EUR", "USD", 100)
        self.assertAlmostEqual(converted_amount_eur, 100 / 0.92)

    def test_unsupported_currency(self):
        """Test handling of unsupported currencies."""
        with self.assertRaises(ValueError):
            self.forex_service.get_rates("XYZ")

        with self.assertRaises(ValueError):
            self.forex_service.convert("USD", "XYZ", 100)

if __name__ == '__main__':
    unittest.main()
