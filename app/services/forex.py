import requests

class ForexService:
    def __init__(self):
        self.base_url = "https://api.exchangerate.host"
        self._mock_rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 157.6,
            "CNY": 7.25,
            "KES": 130.5,
            "AED": 3.67,
            "INR": 83.5
        }

    def get_rates(self, base_currency="USD"):
        """
        Mocks fetching exchange rates.
        In a real application, this would fetch data from a live API.
        """
        if base_currency not in self._mock_rates:
            # In a real app, you might fetch this from the API
            # For the mock, we'll just return an error or default
            raise ValueError(f"Base currency {base_currency} not supported in mock")

        base_rate = self._mock_rates[base_currency]

        rates = {currency: rate / base_rate for currency, rate in self._mock_rates.items()}
        return rates

    def convert(self, from_currency, to_currency, amount):
        """
        Converts an amount from one currency to another using the mock rates.
        """
        rates = self.get_rates(from_currency)
        if to_currency not in rates:
            raise ValueError(f"Target currency {to_currency} not supported")

        conversion_rate = rates[to_currency]
        return amount * conversion_rate
