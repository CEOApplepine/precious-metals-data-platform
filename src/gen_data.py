import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

os.makedirs("data", exist_ok=True)

metals = ["Gold", "Silver", "Platinum", "Palladium"]

# Generate customers
customers = pd.DataFrame({
    "customer_id": range(1, 51),
    "name": [f"Customer {i}" for i in range(1, 51)],
    "country": random.choices(["DE", "AT", "CH", "NL"], k=50)
})
customers.to_csv("data/customers.csv", index=False)

# Generate products
products = pd.DataFrame({
    "product_id": range(1, 5),
    "metal": metals,
    "purity": ["999.9", "999.0", "950", "900"]
})
products.to_csv("data/products.csv", index=False)

# Generate trades
rows = []
start = datetime(2024,1,1)

for i in range(3000):
    rows.append([
        i+1,
        random.choice(metals),
        round(random.uniform(20,60),2),
        random.randint(1,10),
        (start + timedelta(days=random.randint(0,350))).strftime("%Y-%m-%d"),
        random.randint(1, 50)
    ])

df = pd.DataFrame(rows, columns=["trade_id","metal","price","quantity","date","customer_id"])
df.to_csv("data/trades.csv", index=False)

print("Data generated!")
