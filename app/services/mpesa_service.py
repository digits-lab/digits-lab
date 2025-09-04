import time

class MpesaService:
    """
    A mock service to simulate M-Pesa API interactions.
    """

    def initiate_stk_push(self, phone_number, amount):
        """
        Simulates initiating an M-Pesa STK push.
        In a real scenario, this would call the Daraja API and handle callbacks.
        """
        print(f"--- M-PESA MOCK ---")
        print(f"Initiating STK push of KES {amount} to {phone_number}.")
        time.sleep(2)  # Simulate network latency
        print(f"Push sent successfully.")
        print(f"--- END M-PESA MOCK ---")

        # In a real app, we would wait for a callback from M-Pesa.
        # For this mock, we'll just assume it was successful immediately.
        return {"success": True, "message": "STK push initiated successfully."}

    def withdraw_to_mpesa(self, phone_number, amount):
        """
        Simulates a withdrawal from the wallet to an M-Pesa account.
        This would typically be a B2C (Business to Customer) transaction.
        """
        print(f"--- M-PESA MOCK ---")
        print(f"Processing withdrawal of KES {amount} to M-Pesa number {phone_number}.")
        time.sleep(2) # Simulate API call latency
        print(f"Withdrawal successful.")
        print(f"--- END M-PESA MOCK ---")

        return {"success": True, "message": "Withdrawal to M-Pesa successful."}
