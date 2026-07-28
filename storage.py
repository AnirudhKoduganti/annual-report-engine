import json
import os

def save_report(ticker, data):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    with open (f"reports/{ticker}.json", "w", encoding="utf-8") as file:
        return json.dump(data, file, indent=4)

def load_report(ticker):
    with open (f"reports/{ticker}.json", "r", encoding="utf-8") as file:
        return json.load(file)
