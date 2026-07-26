from bs4 import BeautifulSoup
import re
from fetcher import fetch_10k


def extract_sections(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n")

    matches = re.finditer(r"(?m)^Item\s+\d+[A-Z]?\.?", text, re.IGNORECASE)

    items = []

    for match in matches:
        item = match.group().upper()
        start = match.start()

        items.append((item, start))

    item1_pos = []

    for item, start in items:
        if item == "ITEM 1." or item == "ITEM 1":
            item1_pos.append(start)

    item1_start = max(item1_pos) # I did max here because I noticed that the highest character was the official start of the section. 
    # the lower one is usually the table of contents 
    item1a_pos = []

    for item, start in items:
        if item == "ITEM 1A." or item == "ITEM 1A":
            item1a_pos.append(start)

    item1a_start = max(item1a_pos)
    item1b_pos = []

    for item, start in items:
        if item == "ITEM 1B." or item == "ITEM 1B":
            item1b_pos.append(start)

    item1b_start = max(item1b_pos)
    item7_pos = []

    for item, start in items:
        if item == "ITEM 7." or item == "ITEM 7":
            item7_pos.append(start)

    item7_start = max(item7_pos)
    item7a_pos = []

    for item, start in items:
        if item == "ITEM 7A." or item == "ITEM 7A":
            item7a_pos.append(start)

    item7a_start = max(item7a_pos)
    item8_pos = []

    for item, start in items:
        if item == "ITEM 8." or item == "ITEM 8":
            item8_pos.append(start)

    item8_start = max(item8_pos)
    item9_pos = []

    for item, start in items:
        if item == "ITEM 9." or item == "ITEM 9":
            item9_pos.append(start)

    item9_start = max(item9_pos)

    business = text[item1_start:item1a_start]
    risk_factors = text[item1a_start:item1b_start] 
    mda = text[item7_start:item7a_start] 
    financials = text[item8_start:item9_start] 

    return {
        "business": business,
        "risk_factors": risk_factors,
        "mda": mda,
        "financials": financials
    }

# if __name__ == "__main__":
#     report = fetch_10k("AAPL")
#     print(extract_sections(report["html"])["risk_factors"])
