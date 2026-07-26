from fetcher import fetch_10k
from parser import extract_sections
from storage import save_report, load_report

report = fetch_10k("AAPL")

sections = extract_sections(report["html"])

data = {
    "ticker": report["ticker"],
    "company_name": report["company_name"],
    "cik": report["cik"],
    "filing_date": report["filing_date"],
    "fiscal_year": report["fiscal_year"],
    "sections": sections
}

save_report("AAPL", data)

print(load_report("AAPL"))