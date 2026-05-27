import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Smart Sales Analytics Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("SMART SALES ANALYTICS DASHBOARD")

st.markdown("### Sales Data Analysis & Business Insights")

# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

file_path = r"D:\Project\sales-data-cleaning-system\sales-data-cleaning-system\sales_data_sample.xlsx"

df = pd.read_excel(file_path)

# ---------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------

df.columns = df.columns.str.lower().str.replace(' ', '_')

# ---------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------

for col in df.select_dtypes(include='number').columns:
    df[col] = df[col].fillna(df[col].mean())

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

total_sales = df['sales'].sum()
total_orders = df['ordernumber'].nunique()
top_country = df.groupby('country')['sales'].sum().idxmax()
top_product = df.groupby('productline')['sales'].sum().idxmax()

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Top Country", top_country)
col4.metric("Best Product", top_product)

st.markdown("---")

# ---------------------------------------------------
# GRAPH 1 : MONTHLY SALES TREND
# ---------------------------------------------------

monthly_sales = df.groupby('month_id')['sales'].sum()

fig1, ax1 = plt.subplots(figsize=(8, 4))

ax1.plot(monthly_sales.index, monthly_sales.values, marker='o')

ax1.set_title("Monthly Sales Trend")
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales")

st.pyplot(fig1)

# ---------------------------------------------------
# GRAPH 2 : PRODUCT LINE SALES
# ---------------------------------------------------

product_sales = df.groupby('productline')['sales'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(8, 4))

ax2.bar(product_sales.index, product_sales.values)

ax2.set_title("Product Line Sales")
ax2.set_xlabel("Product Line")
ax2.set_ylabel("Sales")

plt.xticks(rotation=45)

st.pyplot(fig2)

# ---------------------------------------------------
# GRAPH 3 : COUNTRY SALES
# ---------------------------------------------------

country_sales = df.groupby('country')['sales'].sum().sort_values(ascending=False).head(5)

fig3, ax3 = plt.subplots(figsize=(8, 4))

ax3.pie(
    country_sales.values,
    labels=country_sales.index,
    autopct='%1.1f%%'
)

ax3.set_title("Top 5 Country Sales")

st.pyplot(fig3)

# ---------------------------------------------------
# GRAPH 4 : SALES DISTRIBUTION
# ---------------------------------------------------

fig4, ax4 = plt.subplots(figsize=(8, 4))

ax4.hist(df['sales'], bins=20)

ax4.set_title("Sales Distribution")
ax4.set_xlabel("Sales")
ax4.set_ylabel("Frequency")

st.pyplot(fig4)

# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------

st.markdown("## Correlation Heatmap")

numeric_cols = df.select_dtypes(include='number')

fig5, ax5 = plt.subplots(figsize=(10, 6))

sns.heatmap(numeric_cols.corr(), annot=True, ax=ax5)

st.pyplot(fig5)

# ---------------------------------------------------
# DATASET PREVIEW
# ---------------------------------------------------

st.markdown("## Dataset Preview")

st.dataframe(df.head(20))

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.markdown("### Developed using Python, Streamlit, Pandas, Matplotlib & Seaborn")