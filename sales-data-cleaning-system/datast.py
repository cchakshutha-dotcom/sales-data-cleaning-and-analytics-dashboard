import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

for col in df.select_dtypes(include=np.number).columns:
    df[col] = df[col].fillna(df[col].mean())

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# ---------------------------------------------------
# CREATE DASHBOARD STYLE MULTIPLE GRAPHS
# ---------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(18, 12))

fig.suptitle("SMART SALES ANALYTICS DASHBOARD", fontsize=22)

# ---------------------------------------------------
# GRAPH 1 : MONTHLY SALES TREND
# ---------------------------------------------------

monthly_sales = df.groupby('month_id')['sales'].sum()

axes[0, 0].plot(monthly_sales.index, monthly_sales.values, marker='o')

axes[0, 0].set_title("Monthly Sales Trend")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Sales")

# ---------------------------------------------------
# GRAPH 2 : TOP PRODUCT SALES
# ---------------------------------------------------

product_sales = df.groupby('productline')['sales'].sum().sort_values(ascending=False)

axes[0, 1].bar(product_sales.index, product_sales.values)

axes[0, 1].set_title("Product Line Sales")
axes[0, 1].set_xlabel("Product Line")
axes[0, 1].set_ylabel("Sales")

axes[0, 1].tick_params(axis='x', rotation=45)

# ---------------------------------------------------
# GRAPH 3 : COUNTRY SALES
# ---------------------------------------------------

country_sales = df.groupby('country')['sales'].sum().sort_values(ascending=False).head(5)

axes[1, 0].pie(
    country_sales.values,
    labels=country_sales.index,
    autopct='%1.1f%%'
)

axes[1, 0].set_title("Top 5 Country Sales")

# ---------------------------------------------------
# GRAPH 4 : SALES DISTRIBUTION
# ---------------------------------------------------

axes[1, 1].hist(df['sales'], bins=20)

axes[1, 1].set_title("Sales Distribution")
axes[1, 1].set_xlabel("Sales")
axes[1, 1].set_ylabel("Frequency")

# ---------------------------------------------------
# FINAL LAYOUT
# ---------------------------------------------------

plt.tight_layout()

plt.show()