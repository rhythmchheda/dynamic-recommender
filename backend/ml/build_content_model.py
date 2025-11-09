"""
Builds and saves the content-based recommendation model using Snowflake's PRODUCTS table.
"""

import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from dotenv import load_dotenv
import snowflake.connector

# =====================================================
# 🔹 Load environment variables
# =====================================================
load_dotenv()

# Snowflake credentials are read securely from .env
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# =====================================================
# 🔹 Connect to Snowflake
# =====================================================
def get_connection():
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"❌ Snowflake connection failed: {e}")

# =====================================================
# 🔹 Load Product Data
# =====================================================
def load_products():
    print("🔹 Loading product data from Snowflake...")

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                PRODUCT_ID,
                TITLE,
                BRAND,
                CATEGORIES,
                MANUFACTURER,
                COLOR,
                IMAGE_URLS,
                PRICE,
                RATING
            FROM PRODUCTS
            WHERE TITLE IS NOT NULL
        """)
        rows = cur.fetchall()
        cols = [col[0] for col in cur.description]
        df = pd.DataFrame(rows, columns=cols)

    print(f"✅ Loaded {len(df)} products from PRODUCTS table")
    return df

# =====================================================
# 🔹 Build TF-IDF + NN model
# =====================================================
def build_model(df):
    print("🔹 Building TF-IDF model...")

    df["TEXT"] = (
        df["TITLE"].fillna("") + " " +
        df["BRAND"].fillna("") + " " +
        df["CATEGORIES"].fillna("") + " " +
        df["MANUFACTURER"].fillna("") + " " +
        df["COLOR"].fillna("")
    )

    vectorizer = TfidfVectorizer(stop_words="english", max_features=6000)
    tfidf_matrix = vectorizer.fit_transform(df["TEXT"])

    print("🔹 Training Nearest Neighbors model...")
    nn_model = NearestNeighbors(metric="cosine", algorithm="brute")
    nn_model.fit(tfidf_matrix)

    return vectorizer, nn_model, df

# =====================================================
# 🔹 Save models
# =====================================================
def save_models(vectorizer, nn_model, df):
    out_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(out_dir, exist_ok=True)

    vect_path = os.path.join(out_dir, "tfidf_vectorizer.joblib")
    nn_path = os.path.join(out_dir, "content_nn.joblib")
    idx_path = os.path.join(out_dir, "product_index_map.joblib")

    index_map = {pid: i for i, pid in enumerate(df["PRODUCT_ID"])}

    joblib.dump(vectorizer, vect_path)
    joblib.dump(nn_model, nn_path)
    joblib.dump(index_map, idx_path)

    print("✅ Model training complete!")
    print(f"📁 Saved vectorizer → {vect_path}")
    print(f"📁 Saved NN model   → {nn_path}")
    print(f"📁 Saved index map  → {idx_path}")

# =====================================================
# 🔹 Main runner
# =====================================================
def main():
    df = load_products()
    vectorizer, nn_model, df = build_model(df)
    save_models(vectorizer, nn_model, df)

if __name__ == "__main__":
    main()
