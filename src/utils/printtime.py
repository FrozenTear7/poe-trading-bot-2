from datetime import datetime


def printtime(message: str):
    now = datetime.now()

    print(f"[{now.strftime('%H:%M:%S')}] {message}")
