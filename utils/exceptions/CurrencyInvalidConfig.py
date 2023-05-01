class CurrencyInvalidConfig(
    Exception,
):
    def __init__(self, currency_name: str, mode: str):
        super().__init__(
            f"Currency: {currency_name}, has invalid config for {mode} mode"
        )
