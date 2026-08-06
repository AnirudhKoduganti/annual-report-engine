import sqlite3 



def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn 


def create_tables(conn):
    cursor = conn.cursor() 

    cursor.execute("""
    create table if not exists companies (
                    ticker TEXT PRIMARY KEY,
                    company_name TEXT,
                    cik TEXT,
                    filing_date TEXT,
                    fiscal_year INTEGER
                    )
""")
    
    cursor.execute("""

    create table if not exists sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,    
                    section_type TEXT, 
                    fiscal_year INTEGER,
                    text TEXT,
                    FOREIGN KEY (ticker) REFERENCES companies(ticker)           
                    )
""")
    conn.commit()