import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta
import sqlite3

st.set_page_config(page_title="Precious Metals Trading Dashboard", layout="wide")
st.title("📊 Precious Metals Trading Dashboard")

# -------------------------------
# Step 1: Create data if missing
# -------------------------------
os.makedirs("data", exist_ok=True)

if not os.path.exists("data/trades.csv"):
    st.info("Generating CSV data...")
    
    metals = ["Gold", "Silver", "Platinum", "Palladium"]

    # Customers
    customers = pd.DataFrame({
        "customer_id": range(1, 51),
        "name": [f"Customer {i}" for i in range(1, 51)],
        "country": random.choices(["DE","AT","CH","NL"], k=50)
    })
    customers.to_csv("data/customers.csv", index=False)

    # Products
    products = pd.DataFrame({
        "product_id": range(1, 5),
        "metal": metals,
        "purity": ["999.9","999.0","950","900"]
    })
    products.to_csv("data/products.csv", index=False)

    # Trades
    rows = []
    start = datetime(2024,1,1)
    for i in range(3000):
        rows.append([
            i+1,
            random.choice(metals),
            round(random.uniform(20,60),2),
            random.randint(1,10),
            (start + timedelta(days=random.randint(0,350))).strftime("%Y-%m-%d"),
            random.randint(1,50)
        ])
    df_trades = pd.DataFrame(rows, columns=["trade_id","metal","price","quantity","date","customer_id"])
    df_trades.to_csv("data/trades.csv", index=False)
    st.success("CSV data generated!")

# -------------------------------
# Step 2: ETL to SQLite
# -------------------------------
DB_PATH = "warehouse.db"

if not os.path.exists(DB_PATH):
    st.info("Running ETL to create warehouse...")
    conn = sqlite3.connect(DB_PATH)

    df_trades = pd.read_csv("data/trades.csv")
    df_customers = pd.read_csv("data/customers.csv")
    df_products = pd.read_csv("data/products.csv")

    df_trades.to_sql("stg_trades", conn, if_exists="replace", index=False)
    df_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
    df_products.to_sql("dim_products", conn, if_exists="replace", index=False)

    df_fact = df_trades.copy()
    df_fact["total_value"] = df_fact["price"] * df_fact["quantity"]
    df_fact.to_sql("fact_trades", conn, if_exists="replace", index=False)
    conn.close()
    st.success("ETL completed!")

# -------------------------------
# Step 3: Load data and show dashboard
# -------------------------------
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM fact_trades", conn)
conn.close()

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Daily Trade Counts")
daily = df.groupby("date").size()
st.line_chart(daily)

st.subheader("Metal Breakdown")
metal_count = df["metal"].value_counts()
st.bar_chart(metal_count)
