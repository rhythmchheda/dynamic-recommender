"""
Dynamic Recommender – ETL Pipeline
----------------------------------
Loads product metadata and user reviews into Snowflake.
Compatible with Windows consoles (no emoji output).
"""

import pandas as pd
import uuid
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

# ----------------------------------------
# 1. Connect to Snowflake
# ----------------------------------------
conn = connect(
    user="RHYTHMCHHEDA",
    password="murtYAK8meZiJCN",
    account="WMHYTLQ-AU37368",
    warehouse="COMPUTE_WH",
    database="DYNAMIC_RECOMMENDER_DB",
    schema="ELECTRONICS_SCHEMA"
)
cursor = conn.cursor()
cursor.execute("USE DATABASE DYNAMIC_RECOMMENDER_DB;")
cursor.execute("USE SCHEMA ELECTRONICS_SCHEMA;")
print("Connected to Snowflake.")

# ----------------------------------------
# 2. Load CSV data
# ----------------------------------------
file_path = r"dynamic-recommender/data/DatafinitiElectronicsProductData.csv"
df = pd.read_csv(file_path)
print("Loaded dataset with shape:", df.shape)

# ----------------------------------------
# 3. Rename and select useful columns
# ----------------------------------------
df = df.rename(columns={
    "id": "product_id",
    "name": "title",
    "brand": "brand",
    "categories": "categories",
    "manufacturer": "manufacturer",
    "colors": "color",
    "imageURLs": "image_urls",
    "dateAdded": "date_added",
    "dateUpdated": "date_updated",
    "dimension": "dimension",
    "weight": "weight",
    "ean": "ean",
    "upc": "upc",
    "reviews.rating": "rating",
    "reviews.text": "review_text",
    "reviews.title": "review_title",
    "reviews.username": "review_username",
    "reviews.date": "review_date"
})

# ----------------------------------------
# 4. Handle missing IDs and generate user IDs
# ----------------------------------------
df["product_id"] = df["product_id"].fillna(df["title"].apply(lambda x: str(uuid.uuid4())[:8]))
df["user_id"] = df["review_username"].fillna("").apply(
    lambda x: str(uuid.uuid4())[:8] if x == "" else str(x)[:8]
)

# ----------------------------------------
# 5. Split into products and interactions
# ----------------------------------------
df_products = df[[
    "product_id", "title", "brand", "categories", "manufacturer", "color",
    "image_urls", "date_added", "date_updated", "dimension", "weight", "ean", "upc"
]].drop_duplicates(subset=["product_id"])

df_interactions = df[[
    "user_id", "product_id", "rating", "review_text", "review_title",
    "review_username", "review_date"
]]

print(f"Products: {df_products.shape}, Interactions: {df_interactions.shape}")

# ----------------------------------------
# 6. Prepare for Snowflake upload
# ----------------------------------------
df_products = df_products.reset_index(drop=True)
df_interactions = df_interactions.reset_index(drop=True)

# Convert all column names to uppercase (matches Snowflake table schema)
df_products.columns = [c.upper() for c in df_products.columns]
df_interactions.columns = [c.upper() for c in df_interactions.columns]

# ----------------------------------------
# 7. Upload to Snowflake
# ----------------------------------------
write_pandas(conn, df_products, table_name="PRODUCTS")
write_pandas(conn, df_interactions, table_name="INTERACTIONS")

print("Upload complete! Data successfully inserted into Snowflake.")
