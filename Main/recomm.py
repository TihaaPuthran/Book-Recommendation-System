import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# ---------------- LOAD DATASET ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "BookDataset", "Bookz.csv")

BOOKS_DF = pd.read_csv(CSV_PATH)

# Keep dataset size reasonable
BOOKS_DF = BOOKS_DF.head(1000)

# Normalize column names (important)
BOOKS_DF.columns = [c.strip() for c in BOOKS_DF.columns]

# ---------------- DETERMINE TEXT FEATURES SAFELY ----------------
text_columns = []

for col in ["Title", "Book-Title", "book_title"]:
    if col in BOOKS_DF.columns:
        TITLE_COL = col
        text_columns.append(col)
        break
else:
    raise Exception("No Title column found in dataset")

for col in ["Author", "Book-Author", "author"]:
    if col in BOOKS_DF.columns:
        text_columns.append(col)
        break

for col in ["Genre", "Category", "Subject"]:
    if col in BOOKS_DF.columns:
        text_columns.append(col)
        break

# Fill missing values
BOOKS_DF[text_columns] = BOOKS_DF[text_columns].fillna("")

# Combine features
BOOKS_DF["combined"] = BOOKS_DF[text_columns].agg(" ".join, axis=1)

# ---------------- VECTORIZE ----------------
vectorizer = CountVectorizer(stop_words="english")
count_matrix = vectorizer.fit_transform(BOOKS_DF["combined"])
similarity = cosine_similarity(count_matrix)

# ---------------- RECOMMENDATION FUNCTION ----------------
def recom(book_name):
    # normalize input
    query = book_name.lower().replace("’", "'").strip()

    # normalize titles
    BOOKS_DF["_norm_title"] = (
        BOOKS_DF[TITLE_COL]
        .str.lower()
        .str.replace("’", "'", regex=False)
        .str.strip()
    )

    # partial / safe match
    matches = BOOKS_DF[BOOKS_DF["_norm_title"].str.contains(query)]

    if matches.empty:
        return ["No similar book found. Try another title from dataset."]

    idx = matches.index[0]

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    return [BOOKS_DF.iloc[i[0]][TITLE_COL] for i in scores]

