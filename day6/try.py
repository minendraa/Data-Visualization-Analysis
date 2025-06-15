import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv('pizza_sales.csv')
    
    # Convert dates and times
    df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, errors='coerce')
    df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S', errors='coerce')
    
    # Extract features
    df['day_of_week'] = df['order_date'].dt.day_name()
    df['hour_of_day'] = df['order_time'].dt.hour
    
    # Create month column as string (fixes the plotting issue)
    df['order_month'] = df['order_date'].dt.strftime('%Y-%m')
    
    return df

df = load_data()

# Calculate metrics
total_sales = df['total_price'].sum()
total_orders = df['order_id'].nunique()
avg_order = total_sales / total_orders if total_orders > 0 else 0

# Dashboard layout
st.title("🍕 Pizza Sales Dashboard")

# Metrics columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")
with col2:
    st.metric("Total Orders", f"{total_orders:,}")
with col3:
    st.metric("Average Order Value", f"${avg_order:,.2f}")

# Monthly Sales Plot
sales_by_month = df.groupby('order_month')['total_price'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=sales_by_month, x='order_month', y='total_price', marker='o')
plt.title("Total Sales Over Time (Monthly)")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
plt.clf()

# Monthly Orders Plot
orders_by_month = df.groupby('order_month')['order_id'].nunique().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=orders_by_month, x='order_month', y='order_id', marker='o', color='red')
plt.title("Total Orders Over Time (Monthly)")
plt.xlabel("Month")
plt.ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
plt.clf()

# Category Sales Plot
category_sales = df.groupby('pizza_category')['total_price'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=category_sales, x='pizza_category', y='total_price', palette='viridis')
plt.title("Sales by Pizza Category")
plt.xlabel("Pizza Category")
plt.ylabel("Total Sales")
st.pyplot(plt.gcf())
plt.clf()

# Size Sales Plot
size_sales = df.groupby('pizza_size')['total_price'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=size_sales, x='pizza_size', y='total_price', palette='coolwarm')
plt.title("Sales by Pizza Size")
plt.xlabel("Pizza Size")
plt.ylabel("Total Sales")
st.pyplot(plt.gcf())
plt.clf()

# Hourly Sales Plot
hourly_sales = df.groupby('hour_of_day')['total_price'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=hourly_sales, x='hour_of_day', y='total_price', marker='o', color='purple')
plt.title("Sales by Hour of the Day")
plt.xlabel("Hour of the Day")
plt.ylabel("Total Sales")
plt.xticks(range(0, 24))
st.pyplot(plt.gcf())
plt.clf()

# Filters in sidebar
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

# Filtered metrics
filtered_total_sales = filtered_df['total_price'].sum()
filtered_total_orders = filtered_df['order_id'].nunique()
filtered_avg_order_value = filtered_total_sales / filtered_total_orders if filtered_total_orders > 0 else 0

st.subheader("Filtered Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Filtered Total Sales", f"${filtered_total_sales:,.2f}")
with col2:
    st.metric("Filtered Total Orders", f"{filtered_total_orders:,}")
with col3:
    st.metric("Filtered Avg Order Value", f"${filtered_avg_order_value:,.2f}")