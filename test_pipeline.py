from fetcher import fetch_10k
from parser import extract_sections
from storage import save_report 

tickers = ["AAPL", "MSFT", "XOM", "JPM", "NVDA"]

for ticker in tickers:
    print(f"\n------{ticker}------")

    report = fetch_10k(ticker)

    if report is None: 
        print(f"Skipping {ticker} because no recent 10-K filing found. ")
        continue 
    
    sections = extract_sections(report["html"])

    data = {
        "ticker": report["ticker"],
        "company_name": report["company_name"],
        "cik": report["cik"],
        "filing_date": report["filing_date"],
        "fiscal_year": report["fiscal_year"],
        "sections": sections
    }

    save_report(ticker, data)
    for section_name, section_text in sections.items():
        print(section_name, len(section_text))