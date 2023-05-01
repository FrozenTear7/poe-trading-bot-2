class CurrencyNotImplemented(
    Exception,
):
    def __init__(self, currency_name: str):
        super().__init__(
            f"Currency: {currency_name}, does not have an implemented config yet or has an invalid name"
        )
