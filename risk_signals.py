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

topics = [
    "tariff",
    "tariffs",
    "supply chain",
    "supply chains",
    "interest rate",
    "interest rates",
    "litigation",
    "inflation",
    "recession",
    "regulation",
    "regulatory",
    "cybersecurity",
    "cyber security",
    "data breach",
    "data breaches",
    "demand",
    "shortage",
    "shortages",
    "foreign exchange",
    "currency",
    "geopolitical",
    "export control",
    "export controls",
    "export restriction",
    "export restrictions",
    "export license",
    "export licenses"
]

realized_terms = [
    "increased",
    "increases",
    "increase",
    "decreased",
    "decreases",
    "decrease",
    "declined",
    "declines",
    "decline",
    "reduced",
    "reduction",
    "reductions",
    "resulted",
    "resulting",
    "caused",
    "incurred",
    "experienced",
    "affected",
    "affect",
    "impact",
    "impacts",
    "impacted",
    "lost",
    "loss",
    "losses",
    "negative",
    "negatively",
    "charge",
    "charges",
    "impairment",
    "impairments",
    "diminished",
    "disrupted",
    "disruption",
    "higher",
    "lower",
    "cost",
    "costs",
    "limited",
    "limits",
    "limiting",
    "restricted",
    "restrictions",
    "prohibited",
    "prevented",
    "unable",
    "unavailable",
    "shortfall",
    "shortfalls",
    "decline",
    "declining"
]

def split_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)

def find_topics(sentence):
    found = []

    sentence_lower = sentence.lower()

    for topic in topics:
        if topic.lower() in sentence_lower:
            if topic not in found:
                found.append(topic)
    return found

def has_realized_terms(sentence):
    sentence = sentence.lower()

    for term in realized_terms:
        if re.search(r"\b" + re.escape(term) + r"\b", sentence):
            return True
    return False

def find_stated_risks(text):
    sentences = split_sentences(text)
    
    risks = []

    for sentence in sentences:
        found_topics = find_topics(sentence)

        if found_topics:
            scores = score_text(sentence)

            if scores["Uncertainty"] >= 2:
                for topic in found_topics:
                    risks.append(
                        {
                            "topic": topic, 
                            "sentence": sentence,
                            "scores": scores
                        }
                    )
    return risks 

def find_realized_events(text):
    sentences = split_sentences(text)
    events = []

    for sentence in sentences:
        found_topics = find_topics(sentence)

        if found_topics:
            scores = score_text(sentence)

            if scores["Negative"] >= 1 and has_realized_terms(sentence):
                for topic in found_topics:
                    events.append(
                        {
                            "topic": topic, 
                            "sentence": sentence, 
                            "scores": scores
                        }
                    )
    return events

stop_words = {
    "the", "and", "that", "this", "with", "from",
    "have", "has", "had", "were", "was", "are",
    "our", "their", "they", "them", "company",
    "companies", "could", "would", "may", "might",
    "will", "can", "been", "being", "into",
    "such", "other", "which", "than", "during",
    "there", "these", "those", "also", "more",
    "less", "because", "including"
}

def get_actual_words(sentence):
    words = re.findall(r"[a-zA-Z]+", sentence.lower())

    actual_words = []

    for word in words:
        if word not in stop_words and len(word) >= 4:
            actual_words.append(word)

    return actual_words

def find_signals(stated_risks, realized_events):
    signals = []

    for risk in stated_risks:
        for event in realized_events:
            if risk["topic"] != event["topic"]:
                continue

            signal_score = risk["scores"]["Uncertainty"] + event["scores"]["Negative"]
            signals.append(
            {
                "topic": risk["topic"],
                "risk_sentence": risk["sentence"],
                "event_sentence": event["sentence"],
                "risk_scores": risk["scores"],
                "event_scores": event["scores"],
                "signal_score": signal_score
            }
        )

    signals.sort(key=lambda x: x["signal_score"], reverse=True)

    return signals 

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

company_data = {}

for row in sections:
    ticker = row["ticker"]

    if ticker not in company_data:
        company_data[ticker] = {
            "risks": [],
            "events": []
        }

    if row["section_type"] == "risk_factors":
        company_data[ticker]["risks"].extend(find_stated_risks(row["text"]))

    if row["section_type"] == "mda":
        company_data[ticker]["events"].extend(find_realized_events(row["text"]))

for ticker in company_data:
    risks = company_data[ticker]["risks"]
    events = company_data[ticker]["events"]

    signals = find_signals(risks, events)

    print(ticker, "Signals:")

    for signal in signals[:10]:
        print("Topic: ", signal["topic"])
        print("Stated Risk: ", signal["risk_sentence"])
        print("Realized Event: ", signal["event_sentence"])
        print("Signal Score: ", signal["signal_score"], "\n")

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

"""

Task 3 Findings: 

The detector identifies stated risks using topic keywords and high LM Uncertainty scores, then searches MD&A for the same topics with 
Negative language and realized-event terms. It successfully produced tariff-related signals for AAPL and several signals for NVDA. MSFT
and JPM had no qualifying signals. 


"""