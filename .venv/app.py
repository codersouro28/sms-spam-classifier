import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import os

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


base_dir = os.path.dirname(os.path.abspath(__file__))

# Correct file path usage
vectorizer_path = os.path.join(base_dir, "vectorizer.pkl")
model_path = os.path.join(base_dir, "model.pkl")
# Get the directory of the current script


# Check if files exist
if not os.path.exists(vectorizer_path):
    raise FileNotFoundError(f"File not found: {vectorizer_path}")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"File not found: {model_path}")

# Load vectorizer
with open(vectorizer_path, "rb") as f:
    tfidf = pickle.load(f)

# Load trained model
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Ensure the model is fitted
if not hasattr(model, "classes_"):
    st.error("The loaded model is not fitted. Train and save the model properly.")
    st.stop()

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    # 1. preprocess
    transformed_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)
    # 4. Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
