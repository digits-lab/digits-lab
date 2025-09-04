from flask import Flask, jsonify
from app.api.wallet import wallet_api
from app.api.rates import rates_api
from app.api.mpesa import mpesa_api
from app.models.wallet import Wallet

# In-memory storage for wallets for demonstration purposes
wallets = {
    "user123": Wallet(user_id="user123", initial_balances={"KES": 10000, "USD": 500})
}

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(wallet_api, url_prefix='/wallet')
    app.register_blueprint(rates_api, url_prefix='/rates')
    app.register_blueprint(mpesa_api, url_prefix='/mpesa')

    # A simple root route
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Multi-Currency Wallet API"})

    return app

# This is for running the app directly for development
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
