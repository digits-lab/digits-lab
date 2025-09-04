import unittest
from app.models.wallet import Wallet

class TestWallet(unittest.TestCase):

    def setUp(self):
        """Set up a new wallet for each test."""
        self.wallet = Wallet(user_id="test_user", initial_balances={"USD": 100, "KES": 10000})

    def test_initial_balances(self):
        """Test that the wallet is initialized with correct balances."""
        self.assertEqual(self.wallet.get_balance("USD"), 100)
        self.assertEqual(self.wallet.get_balance("KES"), 10000)
        self.assertEqual(self.wallet.get_balance("EUR"), 0)

    def test_deposit(self):
        """Test depositing funds."""
        self.wallet.deposit("USD", 50)
        self.assertEqual(self.wallet.get_balance("USD"), 150)

        self.wallet.deposit("EUR", 200)
        self.assertEqual(self.wallet.get_balance("EUR"), 200)

    def test_deposit_negative_amount(self):
        """Test that depositing a negative amount raises an error."""
        with self.assertRaises(ValueError):
            self.wallet.deposit("USD", -50)

    def test_withdraw(self):
        """Test withdrawing funds."""
        self.wallet.withdraw("KES", 5000)
        self.assertEqual(self.wallet.get_balance("KES"), 5000)

    def test_withdraw_insufficient_funds(self):
        """Test that withdrawing more than the balance raises an error."""
        with self.assertRaises(ValueError):
            self.wallet.withdraw("USD", 200)

    def test_withdraw_negative_amount(self):
        """Test that withdrawing a negative amount raises an error."""
        with self.assertRaises(ValueError):
            self.wallet.withdraw("USD", -50)

    def test_convert_sufficient_funds(self):
        """Test currency conversion with sufficient funds."""
        self.wallet.convert("USD", "KES", 50)

        # Check remaining USD balance
        self.assertEqual(self.wallet.get_balance("USD"), 50)

        # Check new KES balance
        # Conversion: 50 USD * 130.5 KES/USD = 6525 KES
        # Initial KES: 10000
        # New KES: 10000 + 6525 = 16525
        self.assertAlmostEqual(self.wallet.get_balance("KES"), 16525)

    def test_convert_insufficient_funds(self):
        """Test currency conversion with insufficient funds."""
        with self.assertRaises(ValueError):
            self.wallet.convert("USD", "KES", 200)

    def test_convert_to_same_currency(self):
        """Test that converting to the same currency raises an error."""
        with self.assertRaises(ValueError):
            self.wallet.convert("USD", "USD", 50)

if __name__ == '__main__':
    unittest.main()
