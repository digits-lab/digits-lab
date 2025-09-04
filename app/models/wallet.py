from app.services.forex import ForexService

class Wallet:
    def __init__(self, user_id, initial_balances=None):
        """
        Initializes a multi-currency wallet for a user.
        :param user_id: The ID of the user owning the wallet.
        :param initial_balances: A dictionary of initial balances, e.g., {"USD": 1000, "KES": 50000}
        """
        self.user_id = user_id
        self.balances = initial_balances if initial_balances is not None else {}
        self.forex_service = ForexService()

    def deposit(self, currency, amount):
        """Adds funds to the wallet."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balances[currency] = self.balances.get(currency, 0) + amount
        return self.get_balance(currency)

    def withdraw(self, currency, amount):
        """Withdraws funds from the wallet."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        current_balance = self.get_balance(currency)
        if current_balance < amount:
            raise ValueError("Insufficient funds.")

        self.balances[currency] = current_balance - amount
        return self.get_balance(currency)

    def get_balance(self, currency):
        """Gets the balance for a specific currency."""
        return self.balances.get(currency, 0)

    def get_all_balances(self):
        """Returns all balances in the wallet."""
        return self.balances

    def convert(self, from_currency, to_currency, amount):
        """
        Converts an amount from one currency to another within the wallet.
        """
        if from_currency == to_currency:
            raise ValueError("Cannot convert to the same currency.")

        if self.get_balance(from_currency) < amount:
            raise ValueError(f"Insufficient balance for {from_currency} to convert.")

        # Withdraw the amount from the source currency
        self.withdraw(from_currency, amount)

        # Get the converted amount using the forex service
        converted_amount = self.forex_service.convert(from_currency, to_currency, amount)

        # Deposit the new amount into the target currency
        self.deposit(to_currency, converted_amount)

        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount_converted": amount,
            "new_balance_of_to_currency": self.get_balance(to_currency)
        }
