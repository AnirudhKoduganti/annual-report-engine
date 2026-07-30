from storage import load_report 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

companies = ["AAPL", "MSFT", "JPM", "NVDA"]

text_train = []
label_train = []

test_text = []
test_label = []

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
label_count = {}

for item in data:
    label = item["label"]
    if label in label_count:
        label_count[label] += 1
    else: 
        label_count[label] = 1

print(label_count)

for item in data:
    if item["company"] == "NVDA":
        test_text.append(item["text"])
        test_label.append(item["label"])
    else:
        text_train.append(item["text"])
        label_train.append(item["label"])

vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(text_train)
test_vectors = vectorizer.transform(test_text)

classifier = MultinomialNB()
classifier.fit(train_vectors, label_train)

predictions = classifier.predict(test_vectors)

index = 0

for label in test_label:
    print("Actual: ", label, "Predicted: ", predictions[index])
    index+=1