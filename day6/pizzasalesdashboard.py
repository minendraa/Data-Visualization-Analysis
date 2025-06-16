import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
import streamlit as st
import datetime as dt

df = pd.read_csv('pizza_sales.csv')

print(df.head())

df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, errors='coerce')
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S', errors='coerce')

df = df.dropna(subset=['order_date', 'order_time'])

df['day_of_week'] = df['order_date'].dt.day_name()
df['hour_of_day'] = df['order_time'].dt.hour

total_sales = df['total_price'].sum()
total_orders = df['order_id'].nunique()
avg_order = total_sales / total_orders if total_orders > 0 else 0

st.title("🍕 Pizza Sales Dashboard")
st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Orders", f"{total_orders:,}")
st.metric("Average Order Value", f"${avg_order:,.2f}")

# Fix 3: Convert to string format for plotting
df['order_month'] = df['order_date'].dt.strftime('%Y-%m')
sales_by_month = df.groupby('order_month')['total_price'].sum().reset_index()

# Sales Over Time
plt.figure(figsize=(10, 6))
sns.lineplot(data=sales_by_month, x='order_month', y='total_price', marker='o')
plt.title("Total Sales Over Time (Monthly)")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
plt.clf()

# Orders Over Time
orders_by_month = df.groupby('order_month')['order_id'].nunique().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=orders_by_month, x='order_month', y='order_id', marker='o', color='red')
plt.title("Total Orders Over Time (Monthly)")
plt.xlabel("Month")
plt.ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
plt.clf()

# Pizza Category Breakdown
category_sales = df.groupby('pizza_category')['total_price'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=category_sales, x='pizza_category', y='total_price', palette='viridis')
plt.title("Sales by Pizza Category")
plt.xlabel("Pizza Category")
plt.ylabel("Total Sales")
st.pyplot(plt.gcf())
plt.clf()

# Pizza Size Breakdown
size_sales = df.groupby('pizza_size')['total_price'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=size_sales, x='pizza_size', y='total_price', palette='coolwarm')
plt.title("Sales by Pizza Size")
plt.xlabel('Pizza Size')
plt.ylabel("Total Sales")
st.pyplot(plt.gcf())
plt.clf()

# Fix 4: Corrected typo in marker parameter
hourly_sales = df.groupby('hour_of_day')['total_price'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=hourly_sales, x='hour_of_day', y='total_price', marker='o', color='purple')
plt.title("Sales by Hour of the Day")
plt.xlabel("Hour of the Day")
plt.ylabel("Total Sales")
plt.xticks(range(0, 24))
st.pyplot(plt.gcf())
plt.clf()

# Fix 5: Corrected date range filter syntax
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['order_date'].min(), df['order_date'].max()],
    min_value=df['order_date'].min(),
    max_value=df['order_date'].max()
)

pizza_category = st.sidebar.selectbox(
    "Select Pizza Category",
    options=['All'] + sorted(df['pizza_category'].unique().tolist())
)

# Apply filters
filtered_df = df[
    (df['order_date'] >= pd.to_datetime(date_range[0])) & 
    (df['order_date'] <= pd.to_datetime(date_range[1]))
]

if pizza_category != 'All':
    filtered_df = filtered_df[filtered_df['pizza_category'] == pizza_category]

filtered_total_sales = filtered_df['total_price'].sum()
filtered_total_orders = filtered_df['order_id'].nunique()
filtered_avg_order_value = filtered_total_sales / filtered_total_orders if filtered_total_orders > 0 else 0

st.subheader("Filtered Results")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Filtered Total Sales", f"${filtered_total_sales:,.2f}")
with col2:
    st.metric("Filtered Total Orders", f"{filtered_total_orders:,}")
with col3:
    st.metric("Filtered Average Order Value", f"${filtered_avg_order_value:,.2f}")




