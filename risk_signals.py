import csv
import re
from db import get_connection

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
cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM sections

""")
sections = [] 

for row in cursor: 
    sections.append(row)

scored_sections = []

for row in sections:
    scores = score_text(row["text"])

    scored_sections.append(
        {
            "ticker": row["ticker"],
            "section_type": row["section_type"],
            "fiscal_year": row["fiscal_year"],
            "scores": scores
        }
    )

for section in scored_sections:
    print(section)

totals = {}

for section in scored_sections:
    section_type = section["section_type"]

    if section_type not in totals:
        totals[section_type] = {
            "Negative": 0, 
            "Uncertainty": 0,
            "count": 0
        }

    totals[section_type]["Negative"] += section["scores"]["Negative"]
    totals[section_type]["Uncertainty"] += section["scores"]["Uncertainty"]
    totals[section_type]["count"] += 1

for section_type in totals:
    negative_avg = totals[section_type]["Negative"] / totals[section_type]["count"]
    uncertainty_avg = totals[section_type]["Uncertainty"] / totals[section_type]["count"]

    print(section_type)
    print("Average Negative: ", negative_avg)
    print("Average Uncertainty: ", uncertainty_avg)

"""
Task 1 Findings: 

Apple's Risk Factors section had substantially higher Negative and Uncertainty scores than its MD&A section. This matches the expectation
that Risk Factors use more language describing potential risks and uncertainty, while MD&A describes actual financial results and events.

"""


"""

Task 2 Findings: 

Risk Factors had the highest average Negative count at 569.0 and the highest average Uncertainty count was 360.5. This matches the expectation
that Risk Factors contain more language describing potential negative outcomes and uncertainty. 

Business sections had the second-highest average Negative and Uncertainty counts, which was somewhat surprising compared with the much lower 
MD&A and Financial averages. These are raw counts, so differences in section length may contribute to the higher counts in longer sections.

"""