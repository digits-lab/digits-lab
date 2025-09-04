from flask import Blueprint, jsonify, request
from app.services.mpesa_service import MpesaService
from app.models.wallet import Wallet

# Again, importing the global 'wallets' dictionary for simplicity.
from app.main import wallets

mpesa_api = Blueprint('mpesa_api', __name__)
mpesa_service = MpesaService()

@mpesa_api.route('/deposit', methods=['POST'])
def mpesa_deposit():
    """
    Simulates a deposit from M-Pesa via STK push.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'phone_number' not in data or 'amount' not in data:
        return jsonify({"error": "Missing user_id, phone_number, or amount"}), 400

    user_id = data['user_id']
    phone_number = data['phone_number']
    amount = float(data['amount'])

    # 1. Initiate STK Push
    stk_response = mpesa_service.initiate_stk_push(phone_number, amount)

    if not stk_response["success"]:
        return jsonify({"error": "M-Pesa STK push failed"}), 500

    # 2. If "successful", credit the user's wallet
    # In a real app, this would be handled by a callback endpoint.
    if user_id not in wallets:
        wallets[user_id] = Wallet(user_id)

    wallet = wallets[user_id]
    wallet.deposit("KES", amount)

    return jsonify({
        "message": "M-Pesa deposit initiated. Wallet credited upon confirmation.",
        "balances": wallet.get_all_balances()
    })

@mpesa_api.route('/withdraw', methods=['POST'])
def mpesa_withdraw():
    """
    Simulates a withdrawal from the wallet to an M-Pesa account.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'phone_number' not in data or 'amount' not in data:
        return jsonify({"error": "Missing user_id, phone_number, or amount"}), 400

    user_id = data['user_id']
    phone_number = data['phone_number']
    amount = float(data['amount'])

    if user_id not in wallets:
        return jsonify({"error": "Wallet not found"}), 404

    wallet = wallets[user_id]

    # 1. Check for sufficient KES balance and withdraw
    try:
        wallet.withdraw("KES", amount)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # 2. Initiate M-Pesa withdrawal
    withdrawal_response = mpesa_service.withdraw_to_mpesa(phone_number, amount)

    if not withdrawal_response["success"]:
        # In a real app, you'd need a reconciliation process to handle this failure.
        # For now, we'll just return an error. A more robust solution would be to
        # re-credit the user's wallet.
        return jsonify({"error": "M-Pesa withdrawal failed after funds were debited."}), 500

    return jsonify({
        "message": "Withdrawal to M-Pesa successful.",
        "balances": wallet.get_all_balances()
    })
