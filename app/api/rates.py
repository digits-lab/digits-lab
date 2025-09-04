from flask import Blueprint, jsonify, request
from app.services.forex import ForexService

rates_api = Blueprint('rates_api', __name__)
forex_service = ForexService()

@rates_api.route('/', methods=['GET'])
def get_all_rates():
    """
    Endpoint to get the latest exchange rates.
    The base currency can be specified with the 'base' query parameter.
    e.g., /rates?base=EUR
    """
    base_currency = request.args.get('base', 'USD')
    try:
        rates = forex_service.get_rates(base_currency)
        return jsonify(rates)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
