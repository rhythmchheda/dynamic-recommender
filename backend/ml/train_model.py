import pandas as pd
import numpy as np
import implicit
from scipy.sparse import coo_matrix
from joblib import dump
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

# -----------------------------------------------------
# 1️⃣ Connect to Snowflake
# -----------------------------------------------------
def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

# -----------------------------------------------------
# 2️⃣ Load data
# -----------------------------------------------------
def fetch_interactions():
    conn = get_connection()
    query = """
        SELECT USER_ID, PRODUCT_ID, COALESCE(RATING, 0) AS RATING
        FROM INTERACTIONS
        WHERE USER_ID IS NOT NULL AND PRODUCT_ID IS NOT NULL
    """
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"✅ Loaded {len(df)} interactions from Snowflake.")
    return df

# -----------------------------------------------------
# 3️⃣ Build a user–item matrix
# -----------------------------------------------------
def build_matrix(df):
    users = df["USER_ID"].astype("category")
    products = df["PRODUCT_ID"].astype("category")

    user_map = dict(enumerate(users.cat.categories))
    item_map = dict(enumerate(products.cat.categories))

    mat = coo_matrix(
        (df["RATING"].astype(float), (users.cat.codes, products.cat.codes))
    )
    return mat.tocsr(), user_map, item_map

# -----------------------------------------------------
# 4️⃣ Train Implicit ALS recommender
# -----------------------------------------------------
def train_als():
    df = fetch_interactions()
    if df.empty:
        print("⚠️ No interaction data found!")
        return

    matrix, user_map, item_map = build_matrix(df)

    model = implicit.als.AlternatingLeastSquares(
        factors=50, regularization=0.01, iterations=15, random_state=42
    )
    model.fit(matrix)

    dump(model, "als_model.joblib")
    dump(user_map, "user_map.joblib")
    dump(item_map, "item_map.joblib")
    print("💾 Model and mappings saved successfully.")

if __name__ == "__main__":
    train_als()
