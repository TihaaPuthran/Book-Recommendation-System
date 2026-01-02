import pickle
import pandas as pd
import numpy as np
import os

# Ensure artifacts folder exists
os.makedirs("artifacts", exist_ok=True)

# Correct path to your CSV file
books_csv = "BookDataset/Bookz.csv"
books = pd.read_csv(books_csv)

# Limit number of books for demonstration (avoid memory crash)
books = books.head(1000)  # <-- use first 1000 rows only

# Create a simple similarity matrix
similarity = np.eye(len(books))

# Save similarity.pkl
with open("artifacts/similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

# Save movie_dict.pkl (dictionary of books)
movie_dict = books.to_dict(orient='records')
with open("artifacts/movie_dict.pkl", "wb") as f:
    pickle.dump(movie_dict, f)

print("Artifacts created successfully!")

