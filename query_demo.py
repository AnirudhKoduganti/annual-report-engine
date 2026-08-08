from db import get_connection, search_by_keyword, get_sections_by_company, get_sections_by_fiscal_year

conn = get_connection("reports.db")

results = search_by_keyword(conn, "tariff", "risk_factors")

for row in results:
    print("Company: ", row["ticker"])
    print("Section: ", row["section_type"])
    print("Preview: ", row["text"][:200], "\n")


results = search_by_keyword(conn, "interest rate", "mda")

for row in results:
    print("Company: ", row["ticker"])
    print("Section: ", row["section_type"])
    print("Preview: ", row["text"][:200], "\n")


companies = ["AAPL", "MSFT", "JPM", "NVDA"]

for company in companies: 
    results = get_sections_by_company(conn, company)

    for row in results:
        if row["section_type"] == "business":
            print("Company: ", row["ticker"])
            print("Section: ", row["section_type"])
            print("Characters: ", len(row["text"]), "\n")


"""
Findings: 

The keyword searches showed that tariff was mentioned in the Risk Factors sections of AAPL, JPM, and NVDA. Interest rate was mentioned in
the MD&A sections of AAPL and NVDA. I found it interesting that tariff appeared as a risk across three different companies, while interest
rate only appeared in two of the companies' MD&A sections. 


"""