import streamlit as st
import pandas as pd
import sqlite3
import os

st.title("Precious Metals Trading Dashboard")

DB_PATH = "warehouse.db"
DATA_DIR = "data"

# Create warehouse DB if not exists
if not os.path.exists(DB_PATH):
    st.info("Running ETL to create warehouse...")
    
    conn = sqlite3.connect(DB_PATH)
    
    # Load CSVs
    df_trades = pd.read_csv(os.path.join(DATA_DIR, "trades.csv"))
    df_customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
    df_products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    
    # Save staging tables
    df_trades.to_sql("stg_trades", conn, if_exists="replace", index=False)
    df_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
    df_products.to_sql("dim_products", conn, if_exists="replace", index=False)
    
    # Create fact table
    df_fact = df_trades.copy()
    df_fact["total_value"] = df_fact["price"] * df_fact["quantity"]
    df_fact.to_sql("fact_trades", conn, if_exists="replace", index=False)
    
    conn.close()
    st.success("ETL completed successfully!")

# Connect to DB and read data
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM fact_trades", conn)
conn.close()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# Simple chart
st.subheader("Daily Trade Counts")
daily = df.groupby("date").size()
st.line_chart(daily)

st.subheader("Metal Breakdown")
metal_count = df["metal"].value_counts()
st.bar_chart(metal_count)
