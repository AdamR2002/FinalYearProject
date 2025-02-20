class Payment:
    def __init__(self, payment_id, user_id, amount, currency, status, method, timestamp):
        self.payment_id = payment_id  # Unique payment ID
        self.user_id = user_id  # Reference to the user who made the payment
        self.amount = amount  # Payment amount
        self.currency = currency  # e.g., "USD", "GBP"
        self.status = status  # "pending", "completed", "failed", "refunded"
        self.method = method  # e.g., "credit_card", "paypal", "bank_transfer"
        self.timestamp = timestamp  # Time when payment was made

    def to_dict(self):
        """ Convert object to dictionary for MongoDB storage. """
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "method": self.method,
            "timestamp": self.timestamp
        }
