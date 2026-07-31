from storage import load_report 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from section_tagger import tag_section


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

rule_predic = []

for text in test_text: 
    rule_predic.append(tag_section(text))

print(classification_report(test_label, predictions))

index = 0

for label in test_label:
    print(
        "Actual: ", label,
        "TF-IDF Prediction: ", predictions[index],
        "Rule-Based Prediction: ", rule_predic[index]
    )
    index+=1

"""
Results: 

The TF-IDF + Naive Bayes classifier correctly identified three out of the four sections for NVDA. It identified the Business, Risk Factors, 
and Financial Statements sections correctly, but incorrectly classified the MD&A section as the Business section. 

The Rule-Based tagger correctly classified the Business and MD&A sections, but misclassified the Risk Factors section as Business. It also
labeled the Financial Statements section as unknown because it was not designed to classify that section. 

Overall, the TF-IDF + Naive Bayes classifier performed better than the Rule-Based tagger on the NVDA test set. However, the small training dataset
of only three companies made it harder for the model to distinguish between Business and MD&A, since those sections can often contain similar
vocabulary

"""