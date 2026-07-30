from storage import load_report 

companies = ["AAPL", "MSFT", "JPM", "NVDA"]

data = []

for company in companies: 
    report = load_report(company)
    
    for section_name, section_text in report["sections"].items():
        data.append(
            {
                "company": company,
                "text": section_text,
                "label": section_name
            }
        )
count = {}

for item in data:
    label = item["label"]
    if label in count:
        count[label] += 1
    else: 
        count[label] = 1

print(count)
