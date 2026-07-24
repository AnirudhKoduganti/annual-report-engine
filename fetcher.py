import requests 
import time 
import os

headers = {
    "User-Agent": "Anirudh Koduganti anirudhkoduganti09@gmail.com"
}


def get_cik(ticker):
    url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=headers)
    time.sleep(0.5)
    data = response.json()  

    for company in data.values():
        if company["ticker"] == ticker.upper():
            return str(company["cik_str"]).zfill(10)
        
    return None 

def get_recent_10k(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=headers)
    time.sleep(0.5)
    data = response.json() 

    forms = data["filings"]["recent"]["form"]
    accession = data["filings"]["recent"]["accessionNumber"]
    primaryDoc = data["filings"]["recent"]["primaryDocument"]

    index = forms.index("10-K")

    return accession[index], primaryDoc[index]

def download_html(cik, accession, document):
    start = 0
    for char in cik: 
        if char == "0":
            start += 1
        else: 
            break 

    cik_new = cik[start:]

    accession_new = accession.replace("-", "")

    url = f"https://www.sec.gov/Archives/edgar/data/{cik_new}/{accession_new}/{document}"

    response = requests.get(url, headers=headers)

    time.sleep(0.5)

    html = response.text 

    return html 


def fetch_10k(ticker):
    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(f"data/{ticker}.html"):
        with open(f"data/{ticker}.html", "r", encoding="utf-8") as file:
            return file.read() 

    cik = get_cik(ticker)
    accession, document = get_recent_10k(cik)
    html = download_html(cik, accession, document)

    with open(f"data/{ticker}.html", "w", encoding="utf-8") as file: 
        file.write(html)

    return html


if __name__ == "__main__":
    html = fetch_10k("AAPL")
    print(html[:500])
    
