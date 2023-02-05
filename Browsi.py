import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# Load the data into a pandas dataframe
data = pd.read_csv("search_data.csv")

# Extract the features using a Tf-idf vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['text'])

# Split the data into training and testing sets
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train a Naive Bayes classifier on the training data
clf = MultinomialNB()
clf.fit(X_train, y_train)

def get_more_relevant_query(query):
    query_vector = vectorizer.transform([query])
    suggested_query = clf.predict(query_vector)
    return suggested_query[0]

def update_response_label(query):
    suggested_query = get_more_relevant_query(query)
    response_label.config(text=suggested_query)
    response_label.update_idletasks()
    label_width = response_label.winfo_width()
    label_height = response_label.winfo_height()
    response_label.config(wraplength=label_width)
    response_frame.config(width=label_width, height=label_height)

root = tk.Tk()
root.title("Query Suggestion")

main_frame = ttk.Frame(root, padding=20)
main_frame.grid(column=0, row=0, sticky="nsew")

query_label = ttk.Label(main_frame, text="Enter query:")
query_label.grid(column=0, row=0, sticky="w")

query_entry = ttk.Entry(main_frame)
query_entry.grid(column=1, row=0, sticky="ew")

response_frame = ttk.Frame(main_frame, padding=10)
response_frame.grid(column=0, row=1, columnspan=2, sticky="ew")

response_label = ttk.Label(response_frame, text="", wraplength=200)
response_label.grid(column=0, row=0)

suggest_button = ttk.Button(main_frame, text="Suggest", command=lambda: update_response_label(query_entry.get()))
suggest_button.grid(column=0, row=2, columnspan=2, pady=10)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_frame.columnconfigure(1, weight=1)

root.mainloop()
