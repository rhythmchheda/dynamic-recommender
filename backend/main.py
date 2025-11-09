from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import os
import logging
import snowflake.connector
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# =====================================================
# 🔹 Setup and Configuration
# =====================================================
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

app = FastAPI(title="Dynamic Recommender API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# 🔹 Snowflake Connection
# =====================================================
def get_connection():
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
        )
        return conn
    except Exception as e:
        logging.error(f"❌ Snowflake connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# =====================================================
# 🔹 Load Pretrained Models
# =====================================================
base_path = os.path.join(os.path.dirname(__file__), "ml", "models")

VECT_PATH = os.path.join(base_path, "tfidf_vectorizer.joblib")
NN_PATH   = os.path.join(base_path, "content_nn.joblib")
IDX_PATH  = os.path.join(base_path, "product_index_map.joblib")

vectorizer = nn_model = idx_map = None
try:
    vectorizer = joblib.load(VECT_PATH)
    nn_model = joblib.load(NN_PATH)
    idx_map = joblib.load(IDX_PATH)

    # ensure it's a dict for O(1) lookup
    if isinstance(idx_map, list):
        idx_map = {pid: i for i, pid in enumerate(idx_map)}

    logging.info(f"✅ Loaded models with {len(idx_map)} products")

except Exception as e:
    logging.warning(f"⚠️ Model loading failed: {e}")

# =====================================================
# 🔹 Utility: Fetch all products from DB
# =====================================================
def fetch_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT PRODUCT_ID, TITLE, BRAND, CATEGORIES, MANUFACTURER, COLOR, IMAGE_URLS, PRICE, RATING
        FROM PRODUCTS
        WHERE TITLE IS NOT NULL
    """)
    df = pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])
    conn.close()

    # Combine text features
    df["TEXT"] = (
        df["TITLE"].fillna("") + " " +
        df["BRAND"].fillna("") + " " +
        df["CATEGORIES"].fillna("") + " " +
        df["MANUFACTURER"].fillna("") + " " +
        df["COLOR"].fillna("")
    )
    return df


# =====================================================
# 🔹 Root Endpoint
# =====================================================
@app.get("/")
def home():
    return {"message": "🚀 Dynamic Recommender API is running successfully!"}


# =====================================================
# 🔹 Get Products
# =====================================================
@app.get("/products")
def get_products(limit: int = 8):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT PRODUCT_ID, TITLE, BRAND, PRICE, RATING, IMAGE_URLS
            FROM PRODUCTS
            WHERE TITLE IS NOT NULL
            QUALIFY ROW_NUMBER() OVER (ORDER BY RANDOM()) <= {limit}
        """)
        df = pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])
        conn.close()
        return df.to_dict(orient="records")

    except Exception as e:
        logging.error(f"❌ Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")


# =====================================================
# 🔹 Recommend Products for a User (Fallback: Top Rated)
# =====================================================
@app.get("/recommend/{user_id}")
def recommend_user(user_id: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT PRODUCT_ID, TITLE, BRAND, PRICE, RATING, IMAGE_URLS
            FROM PRODUCTS
            WHERE RATING IS NOT NULL
            ORDER BY RATING DESC
            LIMIT 8
        """)
        df = pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])
        conn.close()

        logging.info(f"✅ Returned {len(df)} products for user {user_id}")
        return df.to_dict(orient="records")

    except Exception as e:
        logging.error(f"❌ Error recommending for user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# 🔹 Similar Products (Content-based)
# =====================================================
import random

@app.get("/similar/{product_id}")
def get_similar_mock(product_id: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT PRODUCT_ID, TITLE, BRAND, PRICE, RATING, IMAGE_URLS
            FROM PRODUCTS
            WHERE TITLE IS NOT NULL
        """)
        df = pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])
        conn.close()

        # Filter out the clicked product
        df = df[df["PRODUCT_ID"] != product_id]

        # Randomly sample 6 distinct products
        similar_products = df.sample(n=6, replace=False).to_dict(orient="records")

        logging.info(f"🎲 Returning {len(similar_products)} random similar products for {product_id}")
        return similar_products

    except Exception as e:
        logging.error(f"❌ Error fetching mock similar products: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch mock similar products: {e}")