from db import get_connection, create_tables, insert_report
from storage import load_report

companies = ["AAPL", "MSFT", "JPM", "NVDA"]


conn = get_connection("reports.db")

create_tables(conn)


for company in companies: 
    report = load_report(company)

    insert_report(conn, report)

    print(company, "is loaded")