import json

def save_report(ticker, data):
    with open (f"{ticker}.json", "w", encoding="utf-8") as file:
        return json.dump(data, file, indent=4)

def load_report(ticker):
    with open (f"{ticker}.json", "r", encoding="utf-8") as file:
        return json.load(file)
