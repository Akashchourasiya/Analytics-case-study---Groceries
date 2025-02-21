import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title and description of the dashboard
st.title("🍎 Fruit Pricing Dashboard🍊")
st.write("""
This dashboard provides insights into the pricing of apples, oranges, and pears in France, Portugal, and the Netherlands for January 2024.
Use the filters below to explore the data.
""")

# Load the data from Task 1
@st.cache_data  # Cache the data to improve performance
def load_data():
    return pd.read_csv(r'final_fruit.csv')

df = load_data()

# Convert 'beginDate' to datetime for filtering by month
df['beginDate'] = pd.to_datetime(df['beginDate'], format='%d/%m/%Y')
df['month'] = df['beginDate'].dt.month  # Extract month from the date

# Add filters in the sidebar
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['memberStateCode'].unique(),
    default=df['memberStateCode'].unique()
)

selected_products = st.sidebar.multiselect(
    "Select Products",
    options=df['product'].unique(),
    default=df['product'].unique()
)

# Add a month filter
selected_months = st.sidebar.multiselect(
    "Select Months",
    options=df['month'].unique(),
    default=df['month'].unique()
)

selected_varieties = st.sidebar.multiselect(
    "Select Varieties",
    options=df['variety_name'].unique(),
    default=df['variety_name'].unique()
)


# Filter the data based on user selection
filtered_df = df[
    (df['memberStateCode'].isin(selected_countries)) &
    (df['product'].isin(selected_products)) &
    (df['variety_name'].isin(selected_varieties)) &
    (df['month'].isin(selected_months))
]

# Display summary statistics
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", filtered_df.shape[0])
with col2:
    st.metric("Average Price (€)", round(filtered_df['price'].mean(), 2))
with col3:
    st.metric("Unique Varieties", filtered_df['variety_name'].nunique())

# Insight 1: Average prices by country and product
st.subheader("📈 Insight 1: Average Prices by Country and Product")
avg_prices = filtered_df.groupby(['memberStateCode', 'product'])['price'].mean().unstack()

# Create a bar chart using Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
avg_prices.plot(kind='bar', ax=ax)
ax.set_xlabel("Country")
ax.set_ylabel("Average Price (€)")
ax.set_title("Average Fruit Prices by Country")
ax.legend(title="Product")
st.pyplot(fig)

# Insight 2: Price trends over time by country and product
st.subheader("📉 Insight 2: Price Trends Over Time by Country and Product")
if 'beginDate' in filtered_df.columns:
    # Group by date, country, and product to get average prices
    trend_df = filtered_df.groupby(['beginDate', 'memberStateCode', 'product'])['price'].mean().reset_index()
    
    # Create a multi-line chart for price trends
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    for country in selected_countries:
        for product in selected_products:
            subset = trend_df[(trend_df['memberStateCode'] == country) & (trend_df['product'] == product)]
            ax2.plot(subset['beginDate'], subset['price'], label=f"{country} - {product}")
    
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Price (€)")
    ax2.set_title("Fruit Price Trends Over Time by Country and Product")
    ax2.legend(title="Country - Product", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.warning("No date column found for trend analysis.")
    
# Insight 3: Price comparison by country and variety
st.subheader("🌍 Insight 3: Price Comparison by Country and Variety")
price_comparison = filtered_df.groupby(['memberStateCode', 'variety_name'])['price'].mean().unstack()

# Create a heatmap using Seaborn
fig5, ax5 = plt.subplots(figsize=(12, 8))
sns.heatmap(price_comparison, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax5)
ax5.set_xlabel("Variety")
ax5.set_ylabel("Country")
ax5.set_title("Price Comparison by Country and Variety")
st.pyplot(fig5)

# Insight 4: Average prices by variety
st.subheader("🍇 Insight 4: Average Prices by Variety")
avg_prices_variety = filtered_df.groupby('variety_name')['price'].mean().sort_values(ascending=False)

# Create a bar chart for varieties
fig3, ax3 = plt.subplots(figsize=(10, 6))
avg_prices_variety.plot(kind='bar', ax=ax3)
ax3.set_xlabel("Variety")
ax3.set_ylabel("Average Price (€)")
ax3.set_title("Average Prices by Variety")
st.pyplot(fig3)

# Insight 5: Distribution of prices by product
st.subheader("📊 Insight 5: Price Distribution by Product")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_df, x='product', y='price', ax=ax4)
ax4.set_xlabel("Product")
ax4.set_ylabel("Price (€)")
ax4.set_title("Price Distribution by Product")
st.pyplot(fig4)

# Insight 6: Top 5 most expensive varieties
st.subheader("💎 Insight 6: Top 5 Most Expensive Varieties")
top_5_expensive = filtered_df.groupby('variety_name')['price'].mean().nlargest(5)
st.write(top_5_expensive)

# Insight 7: Top 5 cheapest varieties
st.subheader("💰 Insight 7: Top 5 Cheapest Varieties")
top_5_cheapest = filtered_df.groupby('variety_name')['price'].mean().nsmallest(5)
st.write(top_5_cheapest)

filtered_df.drop(filtered_df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

# Display the raw data in an interactive table
st.subheader("📂 Raw Data")
st.dataframe(filtered_df)

# Add a download button for the filtered data
st.subheader("📥 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_fruit_prices.csv",
    mime="text/csv"
)



# Add some styling to make the dashboard more attractive
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)






























