# =========================================================
# SUPERMARKET SALES ANALYSIS PROJECT
# ERROR-FREE STREAMLIT CODE
# =========================================================

# Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================
st.title("🛒 Supermarket Sales Analysis Dashboard")

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    # Read CSV
    df = pd.read_csv("supermarket_sales.csv")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Convert column names to lowercase
    df.columns = df.columns.str.lower()

    return df

df = load_data()

# =========================================================
# SHOW COLUMN NAMES
# =========================================================
st.subheader("📌 Dataset Columns")
st.write(df.columns)

# =========================================================
# DATE CONVERSION
# =========================================================
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])

# =========================================================
# SHOW DATASET
# =========================================================
st.header("📋 Dataset")

if st.checkbox("Show Dataset"):
    st.dataframe(df)

# =========================================================
# DATASET INFO
# =========================================================
st.header("📊 Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])

# Check if total column exists
if "total" in df.columns:
    col3.metric("Total Sales", f"${round(df['total'].sum(),2)}")

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("🔍 Filters")

# City Filter
if "city" in df.columns:
    city = st.sidebar.multiselect(
        "Select City",
        options=df["city"].unique(),
        default=df["city"].unique()
    )
else:
    city = []

# Gender Filter
if "gender" in df.columns:
    gender = st.sidebar.multiselect(
        "Select Gender",
        options=df["gender"].unique(),
        default=df["gender"].unique()
    )
else:
    gender = []

# Payment Filter
if "payment" in df.columns:
    payment = st.sidebar.multiselect(
        "Select Payment Method",
        options=df["payment"].unique(),
        default=df["payment"].unique()
    )
else:
    payment = []

# =========================================================
# FILTER DATA
# =========================================================
filtered_df = df.copy()

if "city" in df.columns:
    filtered_df = filtered_df[filtered_df["city"].isin(city)]

if "gender" in df.columns:
    filtered_df = filtered_df[filtered_df["gender"].isin(gender)]

if "payment" in df.columns:
    filtered_df = filtered_df[filtered_df["payment"].isin(payment)]

# =========================================================
# STATISTICAL SUMMARY
# =========================================================
st.header("📈 Statistical Summary")

st.write(filtered_df.describe())

# =========================================================
# SALES BY CITY
# =========================================================
if "city" in df.columns and "total" in df.columns:

    st.header("🏙️ Sales by City")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.barplot(
        x=filtered_df["city"],
        y=filtered_df["total"],
        estimator=sum,
        palette="viridis",
        ax=ax
    )

    st.pyplot(fig)

# =========================================================
# SALES BY GENDER
# =========================================================
if "gender" in df.columns and "total" in df.columns:

    st.header("👨‍🦰👩 Sales by Gender")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        x=filtered_df["gender"],
        y=filtered_df["total"],
        estimator=sum,
        palette="Set2",
        ax=ax
    )

    st.pyplot(fig)

# =========================================================
# PAYMENT METHOD ANALYSIS
# =========================================================
if "payment" in df.columns:

    st.header("💳 Payment Method Analysis")

    payment_data = filtered_df["payment"].value_counts()

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        payment_data,
        labels=payment_data.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

# =========================================================
# PRODUCT LINE ANALYSIS
# =========================================================
if "product line" in df.columns and "total" in df.columns:

    st.header("🛍️ Product Line Sales")

    fig, ax = plt.subplots(figsize=(12,5))

    sns.barplot(
        x=filtered_df["product line"],
        y=filtered_df["total"],
        estimator=sum,
        palette="coolwarm",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

# =========================================================
# MONTHLY SALES TREND
# =========================================================
if "date" in df.columns and "total" in df.columns:

    st.header("📅 Monthly Sales Trend")

    filtered_df["month"] = filtered_df["date"].dt.month_name()

    monthly_sales = filtered_df.groupby("month")["total"].sum()

    fig, ax = plt.subplots(figsize=(10,5))

    monthly_sales.plot(
        kind="line",
        marker="o",
        linewidth=3,
        ax=ax
    )

    st.pyplot(fig)

# =========================================================
# CUSTOMER RATINGS
# =========================================================
if "rating" in df.columns:

    st.header("⭐ Customer Ratings")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.histplot(
        filtered_df["rating"],
        bins=20,
        kde=True,
        color="purple",
        ax=ax
    )

    st.pyplot(fig)

# =========================================================
# HEATMAP
# =========================================================
st.header("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=np.number)

fig, ax = plt.subplots(figsize=(10,6))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

# =========================================================
# TOP SALES
# =========================================================
if "total" in df.columns:

    st.header("🏆 Top 10 Highest Sales")

    top_sales = filtered_df.nlargest(10, "total")

    st.dataframe(top_sales)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================
st.header("⬇️ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_supermarket_sales.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown("✅ Supermarket Sales Analysis using Streamlit")