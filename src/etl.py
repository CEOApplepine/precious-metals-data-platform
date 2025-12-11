import pandas as pd
import sqlite3

conn = sqlite3.connect("warehouse.db")

# Load CSVs
df_trades = pd.read_csv("data/trades.csv")
df_customers = pd.read_csv("data/customers.csv")
df_products = pd.read_csv("data/products.csv")

df_trades.to_sql("stg_trades", conn, if_exists="replace", index=False)
df_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
df_products.to_sql("dim_products", conn, if_exists="replace", index=False)

# Create fact table
df_fact = df_trades.copy()
df_fact["total_value"] = df_fact["price"] * df_fact["quantity"]
df_fact.to_sql("fact_trades", conn, if_exists="replace", index=False)

conn.close()

print("ETL done!")
