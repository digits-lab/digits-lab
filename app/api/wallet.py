from flask import Blueprint, jsonify, request
from app.models.wallet import Wallet

# This is a simple in-memory storage for wallets.
# In a real application, you would use a database.
# We are importing the 'wallets' object from main.py, which is not ideal,
# but it's a simple way to share data for this example.
# A better approach would be to use a database and a proper application context.
from app.main import wallets


wallet_api = Blueprint('wallet_api', __name__)

@wallet_api.route('/<user_id>/balances', methods=['GET'])
def get_balances(user_id):
    """Get all balances for a user."""
    if user_id not in wallets:
        return jsonify({"error": "Wallet not found"}), 404

    wallet = wallets[user_id]
    return jsonify(wallet.get_all_balances())

@wallet_api.route('/<user_id>/deposit', methods=['POST'])
def deposit(user_id):
    """Deposit funds into a wallet."""
    data = request.get_json()
    if not data or 'currency' not in data or 'amount' not in data:
        return jsonify({"error": "Missing currency or amount"}), 400

    if user_id not in wallets:
        # Create a new wallet if it doesn't exist
        wallets[user_id] = Wallet(user_id)

    wallet = wallets[user_id]
    try:
        currency = data['currency']
        amount = float(data['amount'])
        wallet.deposit(currency, amount)
        return jsonify(wallet.get_all_balances())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@wallet_api.route('/<user_id>/withdraw', methods=['POST'])
def withdraw(user_id):
    """Withdraw funds from a wallet."""
    data = request.get_json()
    if not data or 'currency' not in data or 'amount' not in data:
        return jsonify({"error": "Missing currency or amount"}), 400

    if user_id not in wallets:
        return jsonify({"error": "Wallet not found"}), 404

    wallet = wallets[user_id]
    try:
        currency = data['currency']
        amount = float(data['amount'])
        wallet.withdraw(currency, amount)
        return jsonify(wallet.get_all_balances())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@wallet_api.route('/<user_id>/convert', methods=['POST'])
def convert(user_id):
    """Convert funds from one currency to another."""
    data = request.get_json()
    if not data or 'from_currency' not in data or 'to_currency' not in data or 'amount' not in data:
        return jsonify({"error": "Missing from_currency, to_currency, or amount"}), 400

    if user_id not in wallets:
        return jsonify({"error": "Wallet not found"}), 404

    wallet = wallets[user_id]
    try:
        from_currency = data['from_currency']
        to_currency = data['to_currency']
        amount = float(data['amount'])
        result = wallet.convert(from_currency, to_currency, amount)
        return jsonify({
            "message": "Conversion successful",
            "details": result,
            "balances": wallet.get_all_balances()
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
