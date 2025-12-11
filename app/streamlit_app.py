import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.title("Precious Metals Trading Dashboard")

# Connect DB
conn = sqlite3.connect("warehouse.db")

df = pd.read_sql("SELECT * FROM fact_trades", conn)

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Daily Trade Counts")
daily = df.groupby("date").size()

fig, ax = plt.subplots()
daily.plot(ax=ax)
st.pyplot(fig)

st.subheader("Metal Breakdown")
metal_count = df["metal"].value_counts()
fig2, ax2 = plt.subplots()
metal_count.plot(kind="bar", ax=ax2)
st.pyplot(fig2)

st.info("Data loaded successfully!")
