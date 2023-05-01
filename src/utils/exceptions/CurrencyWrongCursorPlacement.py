class CurrencyWrongCursorPlacement(
    Exception,
):
    def __init__(self):
        super().__init__(
            f"No valid currency in the cursor's place - could not extract info"
        )
