# test_snowflake.py
from dotenv import load_dotenv
import os
import snowflake.connector

load_dotenv()
print("Account:", os.getenv("SNOWFLAKE_ACCOUNT"))

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

print("✅ Connected to Snowflake successfully!")
conn.close()
