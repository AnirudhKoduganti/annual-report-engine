# annual-report-engine

This is week 3 of the summer internship and is a continuation of the last repository. This week focuses on actually taking the things I learned in the prior weeks(and adding new skills) and making a working project out of it. I have started off by writing a detailed analysis of Apple's 10-K so I could better understand the structure. The following is about the code I produced this week. 

## EDGAR Fetcher 
The EDGAR fetcher retrieves a company's most recent 10-K filing from the SEC using its ticker symbol. 

### How it works 

 - Converts a company ticker(such as AAPL) into its SEC CIK.
 - Uses the SEC submissions API to find the company's latest 10-K filing.
 - Downloads the main HTML document for that filing from the SEC archive.
 - Adds a User-Agent header and request delays to follow the SEC API requirements.
 - Caches downloaded filings in the `data/` folder to avoid repeatedly downloading the same report.

### Output
The `fetch_10k(ticker)` function returns a dictionary containing: 

 - `ticker` - company ticker symbol
 - `company_name` - official name of the company from SEC
 - `cik` - SEC identifier for the company
 - `filing_date` - date the 10-K was filed
 - `fiscal_year` - fiscal year covered by the filing
 - `html` - raw HTML content of the 10-K

How to run this file only: 

```python
if __name__ == "__main__":
  report = fetch_10k("`company_ticker`")
  print(report["html"][:500]) # Prints the first 500 characters of the html

```
### Limitations
 - The fetcher only searches the SEC's recent filing list. If a company's 10-K is not found in this list(ex. XOM), it will not return it and continue


## 10-K Section Extractor 

The section parser extracts important sections from the raw HTML of a 10-K filing and organizes them into a structured dictionary. 

### How it works 

 - Converts the HTML filing into plain text using BeautifulSoup
 - Searches the document for SEC Item Headings using regex.
 - Finds the following important sections:
     - Item 1 - Business
     - Item 1A - Risk Factors
     - Item 7 - Management's Discussion and Analysis(MD&A)
     - Item 8 - Financial Statements
  - Handles duplicate Item headings by selecting the last occurrence(using `max()`), since earlier matches are usually located in the table of contents.
  - Uses the next Item's heading as an ending boundary for each section
  - Returns the extracted sections as a dictionary

### Output

The `extract_sections(html)` function returns: 

```python
{
  "business": business,
  "risk_factors": risk_factors,
  "mda": mda,
  "financials": financials
}
```

How to run this file only: 

#### Make sure to import `fetch_10k` from fetcher


```python
  if __name__ == "__main__":
    report = fetch_10k("AAPL")
    print(extract_sections(report["html"])["risk_factors"])
```

### Limitations
 - The parser only works on headings that have a period or nothing after the heading(`ITEM 1A. ITEM 1A`). It does not work only semi colons, so the parser could skip over that part if there was a 10-K that used semicolons for the section heading.
 - Since the parser uses Item numbers for boundaries, it can output the incorrect text when those item numbers are missing in different 10-Ks
 - Parser can break if 10-K contains duplicate headings in the tale of contents. For these documents, it may not identify the true start of the section. 

## JSON Storage 

The storage file saves extracted 10-K data as JSON files and lets saved reports be opened later without running the fetcher and parser again. 

### How it works 

 - Takes the structured report data that is made by the pipeline.
 - Saves the data into a JSON file using the company's ticker as the filename.
 - Store the output in a readable format with indentation.
 - Allows saved reports to be loaded back into Python using the ticker.

### Output 

Each JSON file contains:
 - `ticker`
 - `company_name`
 - `cik`
 - `filing_date`
 - `fiscal_year`
 - `sections`

where `sections` has the extracted sections from before. 

How to run this file: 

 - It is recommended to create a different python file that tests only the output of the storage.py file.
For example:

 ```python
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
```

## Putting together all the files to test on different companies 
This is the final step of the project. You can use all the elements of the different files to gather data to output. 

## What the full pipeline does 

This python pipeline retrieves a company's 10-K filings from the SEC EDGAR system, extracts important sections, and saves the results as structured JSON files. 

## Output
The output on the console contains a iteration of the 5 companies listed in the test pipeline and how many characters each section is. 

## Limitations
 - The program skips over XOM because there are no 10-K filings listed in the `recent` folder from the SEC.
 - The parser relies on Item numbers and regular expressions, so unusual filing structures may cause extraction errors
 - Some extracted sections may be too short or contain text from nearby sections if the wrong item heading is detected.
 - Financial Statements extraction is less reliable because Item 8 formatting varies significantly between companies

## How to run everything 

Install the required libraries located in the requirements.txt

```bash
pip install -r requirements.txt
```

Then, download all the files listed and run the test_pipeline.py. You can customize which tickers to use to your own liking. 
