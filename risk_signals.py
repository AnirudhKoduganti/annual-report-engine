import csv
import re
from db import get_connection, get_sections_by_company  

lm_dict = {}

with open ("Loughran-McDonald_MasterDictionary_1993-2025.csv", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        lm_dict[row["Word"]] = row

def score_text(text):
    count = {
        "Negative": 0, 
        "Positive": 0, 
        "Uncertainty": 0,
        "Litigious": 0,
        "Strong_Modal": 0, 
        "Constraining": 0
    }

    words = text.upper().split()
    cleaned_words = []

    for word in words:
        word = re.sub(r"[^A-Z]", "", word)
        cleaned_words.append(word)

    for word in cleaned_words:
        if word in lm_dict:
            for category in count:
                if int(lm_dict[word][category]) > 0:
                    count[category] += 1

    return count 

conn = get_connection("reports.db")

sections = get_sections_by_company(conn, "AAPL")  

for row in sections: 
    if row["section_type"] == "risk_factors":
        print("Risk Factors:", score_text(row["text"]))

    if row["section_type"] == "mda":
        print("MD&A:", score_text(row["text"]))


"""
Task 1 Findings: 

Apple's Risk Factors section had substantially higher Negative and Uncertainty scores than its MD&A section. This matches the expectation
that Risk Factors use more language describing potential risks and uncertainty, while MD&A describes actual financial results and events.

"""