
risk_words = {
    "risk", "risks", "may", "could", "uncertain", "uncertainty", "adverse", "material adverse", "material adverse impact",
    "materially adversely affect", "tariffs", "trade", "trade disputes", "supply chain", "cybersecurity", "litigation",
    "compliance", "regulatory", "restrictions", "imports", "exports", "economic", "geopolitical"
}

mda_words = {
    "revenue", "gross margin", "gross profit", "net sales", "operating income", "operating expenses", "results of operations",
    "financial condition", "cash flow", "inventory", "inventory provisions", "customer demand", "manufacturing",
    "lead times", "pricing", "pricing actions", "capacity", "yield", "cost", "costs", "expenses", "income", "cash",
    "assets", "liabilities", "debt", "equity"
}

business_words = {
    "business", "company", "products", "product", "services",
    "customers", "technology", "platform", "software","architecture", "architectures", "gpu", "cpu", "dpu", 
    "ai", "artificial intelligence", "networking", "systems", "launch", "launched","develop", "development",
    "research", "engineering", "design", "manufacture", "manufacturing", "innovation", "headquarters", "employees"
}

def tag_section(text):
    risk_count = 0 
    mda_count = 0
    business_count = 0 
    text = text.lower() 

    for word in risk_words:
        if word in text:
            risk_count += 1
    
    for word in mda_words:
        if word in text:
            mda_count += 1

    for word in business_words:
        if word in text:
            business_count += 1

    if risk_count == 0 and mda_count == 0 and business_count == 0: 
        return "unknown"
    elif risk_count > mda_count and risk_count > business_count:
        return "risk_factor"
    elif mda_count > risk_count and mda_count > business_count:
        return "mda"
    elif business_count > risk_count and business_count > mda_count:
        return "business"
    return "unknown"

def read_paragraph(filename):
    with open(filename, "r", encoding="utf-8") as file:  
        return file.read() 
    
tests = {
    read_paragraph("paragraphs/business1.txt"): "business",
    read_paragraph("paragraphs/business2.txt"): "business",
    read_paragraph("paragraphs/business3.txt"): "business",
    read_paragraph("paragraphs/business4.txt"): "business",
    read_paragraph("paragraphs/risk1.txt"): "risk_factor",
    read_paragraph("paragraphs/risk2.txt"): "risk_factor",
    read_paragraph("paragraphs/risk3.txt"): "risk_factor",
    read_paragraph("paragraphs/mda1.txt"): "mda",
    read_paragraph("paragraphs/mda2.txt"): "mda",
    read_paragraph("paragraphs/mda3.txt"): "mda",
}

correct = 0

for paragraph, expected in tests.items():
    predict = tag_section(paragraph) 
    print("Expected: ", expected)
    print("Prediction: ", predict, "\n")

    if predict == expected:
        correct += 1

accuracy = (correct / len(tests)) * 100 

print("You got ", correct, " correct out of ", len(tests), "tests.")
print("Your accuracy is: ", accuracy, "%")