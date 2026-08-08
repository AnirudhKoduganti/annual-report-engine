import sqlite3 


def create_tables(conn):
    cursor = conn.cursor() 

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
                    ticker TEXT PRIMARY KEY,
                    company_name TEXT,
                    cik TEXT,
                    filing_date TEXT,
                    fiscal_year INTEGER
                    )
""")
    
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,    
                    section_type TEXT, 
                    fiscal_year INTEGER,
                    text TEXT,
                    FOREIGN KEY (ticker) REFERENCES companies(ticker)           
                    )
""")
    conn.commit()


def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn 


def insert_report(conn, report_data):
    cursor = conn.cursor()


    cursor.execute(""" 
        INSERT OR REPLACE INTO companies 
        (ticker, company_name, cik, filing_date, fiscal_year)
        VALUES (?, ?, ?, ?, ?) 
    
    """, (
        report_data["ticker"], 
        report_data["company_name"],
        report_data["cik"],
        report_data["filing_date"],
        report_data["fiscal_year"]
    ))

    for section_type, text in report_data["sections"].items():
        cursor.execute(""" 
            INSERT INTO sections
            (ticker, section_type, fiscal_year, text)
            VALUES (?, ?, ?, ?)
                       """, (
                           report_data["ticker"],
                           section_type, 
                           report_data["fiscal_year"],
                           text
                       ))
        
    conn.commit()


def search_by_keyword(conn, keyword, section_type=None):
    cursor = conn.cursor()

    if section_type:
        cursor.execute("""
            SELECT * 
            FROM sections
            WHERE text LIKE ? 
            AND section_type = ?
            """, (f"%{keyword}%", section_type))
        
    else:
        cursor.execute("""
                        SELECT * 
                        FROM sections
                        WHERE text LIKE ?
                        """, (f"%{keyword}%",))
                       
    rows = []

    for row in cursor: 
        rows.append(row)

    return rows 


def get_sections_by_company(conn, ticker):
    cursor = conn.cursor()

    cursor.execute("""
                    SELECT *
                    FROM sections
                    WHERE ticker = ?
                    """, (ticker,))
                           
                   
    rows = []

    for row in cursor:
        rows.append(row)

    return rows 

def get_sections_by_fiscal_year(conn, fiscal_year):
    cursor = conn.cursor()

    cursor.execute("""
                    SELECT *
                    FROM sections
                    WHERE fiscal_year = ?
                    """, (fiscal_year,))
                   
    rows = []

    for row in cursor:
        rows.append(row)


    return rows
