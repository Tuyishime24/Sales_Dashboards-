import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Global Superstore Executive BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Corporate Theme

PRIMARY = "#1E3A8A"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
BG = "#F8FAFC"

# Executive CSS
st.markdown("""
<style>

.main{
    background-color:#F8FAFC;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

[data-testid="stSidebar"]{
    background:#0F172A;
}

[data-testid="stSidebar"] *{
    color:white;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:18px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    border-left:6px solid #2563EB;
}

div[data-testid="stPlotlyChart"]{
    background:white;
    border-radius:15px;
    padding:10px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# Data Loading

@st.cache_data
def load_data():

    df = pd.read_csv("superstore.csv.zip")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_")
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    df["ship_date"] = pd.to_datetime(
        df["ship_date"],
        errors="coerce"
    )

    df["month"] = (
        df["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    return df

df = load_data()

# Formate function

def format_currency(value):
    """Format large currency values"""
    
    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    
    elif value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    
    elif value >= 1_000:
        return f"${value/1_000:.2f}K"
    
    return f"${value:,.0f}"


def format_number(value):
    """Format large numbers"""
    
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    
    return f"{value:,.0f}"


def format_percent(value):
    return f"{value:.2f}%"


# Executive Header
st.markdown(f"""
<div style="
background:linear-gradient(90deg,#0F172A,#1E40AF);
padding:30px;
border-radius:20px;
color:white;
">

<h1>📊 Global Superstore Executive BI Dashboard</h1>

<p style="font-size:18px;">
Business Intelligence Analytics Platform
</p>

<p>
Executive insights into Sales, Profitability,
Customer Performance, Geographic Trends and Operations
</p>

<p>
Last Updated:
{datetime.now().strftime('%d %B %Y %H:%M')}
</p>

</div>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.markdown("""
# 🎛 Executive Control Center

Use the filters below to analyze
business performance across markets,
regions, products and customer segments.
""")

st.sidebar.markdown("---")

st.sidebar.metric(
    "🌎 Countries",
    df["country"].nunique()
)

st.sidebar.metric(
    "📦 Products",
    df["product_id"].nunique()
)

st.sidebar.metric(
    "👥 Customers",
    df["customer_id"].nunique()
)


with st.sidebar.expander("📅 Time Filters", expanded=True):

    year = st.multiselect(
        "Year",
        sorted(df["year"].unique()),
        sorted(df["year"].unique())
    )

with st.sidebar.expander("🌍 Geography", expanded=True):

    market = st.multiselect(
        "Market",
        sorted(df["market2"].unique()),
        sorted(df["market2"].unique())
    )

    region = st.multiselect(
        "Region",
        sorted(df["region"].unique()),
        sorted(df["region"].unique())
    )

    country = st.multiselect(
        "Country",
        sorted(df["country"].unique()),
        sorted(df["country"].unique())
    )

with st.sidebar.expander("📦 Products", expanded=True):

    category = st.multiselect(
        "Category",
        sorted(df["category"].unique()),
        sorted(df["category"].unique())
    )

with st.sidebar.expander("👥 Customers", expanded=True):

    segment = st.multiselect(
        "Segment",
        sorted(df["segment"].unique()),
        sorted(df["segment"].unique())
    )

    st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Active Selection")

st.sidebar.write(
    f"Years: {len(year)}"
)

st.sidebar.write(
    f"Markets: {len(market)}"
)

st.sidebar.write(
    f"Regions: {len(region)}"
)

st.sidebar.write(
    f"Countries: {len(country)}"
)

if st.sidebar.button("🔄 Reset Dashboard"):
    st.rerun()


# Filter Data

filtered_df = df[
    (df["year"].isin(year)) &
    (df["market2"].isin(market)) &
    (df["region"].isin(region)) &
    (df["country"].isin(country)) &
    (df["category"].isin(category)) &
    (df["segment"].isin(segment))
]

# Executive KPI Cards

sales = filtered_df["sales"].sum()

profit = filtered_df["profit"].sum()

orders = filtered_df["order_id"].nunique()

customers = filtered_df["customer_id"].nunique()

quantity = filtered_df["quantity"].sum()

avg_discount = filtered_df["discount"].mean()*100

profit_margin = (
    profit/sales*100
    if sales else 0
)

avg_order_value = (
    sales/orders
    if orders else 0
)

st.subheader("📈 Executive KPIs")

k1,k2,k3,k4 = st.columns(4)

k5,k6,k7,k8 = st.columns(4)

k1.metric(
    "💰 Total Sales",
    format_currency(sales)
)

k2.metric(
    "📈 Total Profit",
    format_currency(profit)
)

k3.metric(
    "🎯 Profit Margin",
    format_percent(profit_margin)
)

k4.metric(
    "🧾 Orders",
    format_number(orders)
)

k5.metric(
    "👥 Customers",
    format_number(customers)
)

k6.metric(
    "📦 Quantity Sold",
    format_number(quantity)
)

k7.metric(
    "💵 Avg Order Value",
    format_currency(avg_order_value)
)

k8.metric(
    "🏷 Avg Discount",
    format_percent(avg_discount)

)

# ==========================================
# DASHBOARD HEALTH PANEL
# ==========================================

st.markdown("---")

st.subheader("📌 Business Overview")

c1, c2, c3, c4 = st.columns(4)

c1.info(
    f"""
    🌍 Countries

    {filtered_df['country'].nunique()}
    """
)

c2.info(
    f"""
    👥 Customers

    {format_number(customers)}
    """
)

c3.info(
    f"""
    📦 Products

    {filtered_df['product_id'].nunique()}
    """
)

c4.info(
    f"""
    🧾 Orders

    {format_number(orders)}
    """
)


# Sales & Profit Intelligence
st.markdown("---")
st.subheader("📈 Sales & Profit Intelligence")

# Prepare Monthly Data
monthly = (
    filtered_df
    .groupby("month")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
)

# Executive Charts
col1, col2 = st.columns(2)

# Sales Trend
with col1:

    fig = px.line(
        monthly,
        x="month",
        y="sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig.update_layout(
        height=450,
        title_x=0.05,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Profit Trend

with col2:

    fig = px.line(
        monthly,
        x="month",
        y="profit",
        markers=True,
        title="Monthly Profit Trend"
    )

    fig.update_layout(
        height=450,
        title_x=0.05,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Executive Insight Box

    sales_growth = (
    (monthly["sales"].iloc[-1] -
     monthly["sales"].iloc[0])
    /
    monthly["sales"].iloc[0]
    *100
)

profit_growth = (
    (monthly["profit"].iloc[-1] -
     monthly["profit"].iloc[0])
    /
    monthly["profit"].iloc[0]
    *100
)

st.success(
    f"""
    📈 Sales Growth: {sales_growth:.1f}%

    💰 Profit Growth: {profit_growth:.1f}%

    Executive Observation:
    The business shows a positive long-term performance trend across the selected period.
    """
)

# ==========================================
# GEOGRAPHIC INTELLIGENCE
# ==========================================

st.markdown("---")
st.subheader("🌍 Geographic Intelligence")

# Market Analysis + Region Analysis

market_sales = (
    filtered_df
    .groupby("market2")["sales"]
    .sum()
    .reset_index()
    .sort_values("sales", ascending=False)
)

region_sales = (
    filtered_df
    .groupby("region")["sales"]
    .sum()
    .reset_index()
    .sort_values("sales", ascending=False)
)

col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        market_sales,
        names="market2",
        values="sales",
        hole=0.60,
        title="Market Contribution"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



with col2:

    fig = px.bar(
        region_sales,
        x="region",
        y="sales",
        color="sales",
        title="Regional Sales Performance"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Top Countries

country_sales = (
    filtered_df
    .groupby("country")["sales"]
    .sum()
    .reset_index()
    .sort_values("sales", ascending=False)
    .head(15)
)


fig = px.bar(
    country_sales,
    x="sales",
    y="country",
    orientation="h",
    title="Top 15 Countries by Sales",
    color="sales"
)

fig.update_layout(
    height=550,
    yaxis={"categoryorder":"total ascending"}
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Interactive World Map

country_map = (
    filtered_df
    .groupby("country")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
)

# Create Map

fig = px.choropleth(
    country_map,
    locations="country",
    locationmode="country names",
    color="sales",
    hover_name="country",
    hover_data=["profit"],
    title="Global Sales Distribution"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Geographic Insights Panel

best_market = (
    market_sales
    .sort_values("sales", ascending=False)
    .iloc[0]["market2"]
)

best_region = (
    region_sales
    .sort_values("sales", ascending=False)
    .iloc[0]["region"]
)

best_country = (
    country_sales
    .sort_values("sales", ascending=False)
    .iloc[0]["country"]
)


st.success(
    f"""
    🌍 Best Performing Market: {best_market}

    🗺 Highest Revenue Region: {best_region}

    🏆 Top Revenue Country: {best_country}

    Executive Insight:
    Geographic performance indicates strong revenue concentration in key international markets.
    """
)


# ==========================================
# PRODUCT INTELLIGENCE
# ==========================================

st.markdown("---")
st.subheader("📦 Product Intelligence")

# Prepare Product Data
category_summary = (
    filtered_df
    .groupby("category")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
)

subcategory_summary = (
    filtered_df
    .groupby("sub_category")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
)

# Category Performance

# Sales by Category
# Profit by Category

col1, col2 = st.columns(2)

# Sales

with col1:

    fig = px.bar(
        category_summary,
        x="category",
        y="sales",
        color="sales",
        title="Category Revenue Performance"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Profit

with col2:

    fig = px.bar(
        category_summary,
        x="category",
        y="profit",
        color="profit",
        title="Category Profitability"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Sub-Category Performance

fig = px.bar(
    subcategory_summary.sort_values(
        "sales",
        ascending=False
    ),
    x="sub_category",
    y="sales",
    color="profit",
    title="Sub-Category Performance"
)

fig.update_layout(
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Top Products
top_products = (
    filtered_df
    .groupby("product_name")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
    .sort_values("sales", ascending=False)
    .head(10)
)


fig = px.bar(
    top_products,
    x="sales",
    y="product_name",
    orientation="h",
    color="profit",
    title="Top 10 Revenue Generating Products"
)

fig.update_layout(
    height=550,
    yaxis={
        "categoryorder":"total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Bottom Products

bottom_products = (
    filtered_df
    .groupby("product_name")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
    .sort_values("profit")
    .head(10)
)

fig = px.bar(
    bottom_products,
    x="profit",
    y="product_name",
    orientation="h",
    color="profit",
    title="Bottom 10 Products by Profit"
)

fig.update_layout(
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Product Intelligence KPIs

best_category = (
    category_summary
    .sort_values("sales", ascending=False)
    .iloc[0]["category"]
)

most_profitable_category = (
    category_summary
    .sort_values("profit", ascending=False)
    .iloc[0]["category"]
)

best_product = (
    top_products
    .iloc[0]["product_name"]
)


c1, c2, c3 = st.columns(3)

c1.success(
    f"""
    🏆 Top Category

    {best_category}
    """
)

c2.success(
    f"""
    💰 Most Profitable

    {most_profitable_category}
    """
)

c3.success(
    f"""
    ⭐ Best Product

    {best_product}
    """
)


# Executive Product Insights

st.markdown("### 🧠 Product Intelligence Insights")


st.success(
    f"""
    ✔ {best_category} generates the highest revenue.

    ✔ {most_profitable_category} contributes the highest profit.

    ✔ {best_product} is currently the strongest performing product.

    ✔ Several low-profit products require review to improve margins.

    ✔ Product portfolio optimization could increase overall profitability.
    """
)

# Strategic Recommendations

st.markdown("### 🎯 Product Strategy Recommendations")

st.info(
    f"""
    1. Increase inventory investment in {best_category}.

    2. Expand marketing campaigns around high-performing products.

    3. Review pricing strategies for underperforming products.

    4. Reduce discount levels on low-margin products.

    5. Focus sales efforts on profitable sub-categories.
    """
)

# 👥 Customer Intelligence

# ==========================================
# CUSTOMER INTELLIGENCE
# ==========================================

st.markdown("---")
st.subheader("👥 Customer Intelligence")

# Prepare Customer Data

customer_summary = (
    filtered_df
    .groupby("customer_name")
    .agg({
        "sales":"sum",
        "profit":"sum",
        "order_id":"nunique"
    })
    .reset_index()
)

segment_summary = (
    filtered_df
    .groupby("segment")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
)

# Segment Performance

col1, col2 = st.columns(2)



# Revenue by Segment

with col1:

    fig = px.pie(
        segment_summary,
        names="segment",
        values="sales",
        hole=0.6,
        title="Revenue by Customer Segment"
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Profit by Segment


with col2:

    fig = px.bar(
        segment_summary,
        x="segment",
        y="profit",
        color="profit",
        title="Profit by Customer Segment"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Top Customers

top_customers = (
    customer_summary
    .sort_values("sales", ascending=False)
    .head(10)
)


fig = px.bar(
    top_customers,
    x="sales",
    y="customer_name",
    orientation="h",
    color="profit",
    title="Top 10 Customers by Revenue"
)

fig.update_layout(
    height=550,
    yaxis={
        "categoryorder":"total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Most Profitable Customers

top_profit_customers = (
    customer_summary
    .sort_values("profit", ascending=False)
    .head(10)
)



fig = px.bar(
    top_profit_customers,
    x="profit",
    y="customer_name",
    orientation="h",
    color="profit",
    title="Top 10 Most Profitable Customers"
)

fig.update_layout(
    height=550,
    yaxis={
        "categoryorder":"total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Customer Revenue vs Profit

top50 = (
    customer_summary
    .sort_values("sales", ascending=False)
    .head(50)
)



fig = px.scatter(
    top50,
    x="sales",
    y="profit",
    size="order_id",
    hover_name="customer_name",
    title="Customer Revenue vs Profitability"
)

fig.update_layout(height=600)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Customer Intelligence KPI Panel


best_customer = (
    customer_summary
    .sort_values("sales", ascending=False)
    .iloc[0]["customer_name"]
)

most_profitable_customer = (
    customer_summary
    .sort_values("profit", ascending=False)
    .iloc[0]["customer_name"]
)

best_segment = (
    segment_summary
    .sort_values("sales", ascending=False)
    .iloc[0]["segment"]
)


c1, c2, c3 = st.columns(3)

c1.success(
    f"""
    🏆 Top Customer

    {best_customer}
    """
)

c2.success(
    f"""
    💰 Most Profitable Customer

    {most_profitable_customer}
    """
)

c3.success(
    f"""
    👥 Best Segment

    {best_segment}
    """
)


# Executive Customer Insights

st.markdown("### 🧠 Customer Intelligence Insights")

st.success(
    f"""
    ✔ {best_segment} contributes the largest share of revenue.

    ✔ {best_customer} is the highest revenue-generating customer.

    ✔ {most_profitable_customer} delivers the highest profitability.

    ✔ Revenue concentration among top customers suggests strong account management opportunities.

    ✔ Customer profitability analysis can improve retention strategies and resource allocation.
    """
)


# Strategic Recommendations


st.markdown("### 🎯 Customer Strategy Recommendations")

st.info(
    f"""
    1. Develop loyalty programs for top customers.

    2. Increase engagement with high-profit customer accounts.

    3. Create targeted campaigns for the {best_segment} segment.

    4. Identify opportunities to grow mid-tier customer accounts.

    5. Monitor customer profitability, not just sales volume.
    """
)


# Operational Intelligence

# ==========================================
# OPERATIONAL INTELLIGENCE
# ==========================================

st.markdown("---")
st.subheader("🚚 Operational Intelligence")


# Prepare Operational Data


ship_mode_summary = (
    filtered_df
    .groupby("ship_mode")
    .agg({
        "sales":"sum",
        "profit":"sum",
        "shipping_cost":"sum"
    })
    .reset_index()
)

priority_summary = (
    filtered_df
    .groupby("order_priority")
    .agg({
        "sales":"sum",
        "profit":"sum"
    })
    .reset_index()
)

shipping_region = (
    filtered_df
    .groupby("region")
    .agg({
        "shipping_cost":"sum"
    })
    .reset_index()
    .sort_values(
        "shipping_cost",
        ascending=False
    )
)


# Ship Mode Analysis

col1, col2 = st.columns(2)


# Sales by Ship Mode

with col1:

    fig = px.bar(
        ship_mode_summary,
        x="ship_mode",
        y="sales",
        color="sales",
        title="Sales by Shipping Method"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Profit by Ship Mode

with col2:

    fig = px.bar(
        ship_mode_summary,
        x="ship_mode",
        y="profit",
        color="profit",
        title="Profit by Shipping Method"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Shipping Cost Analysis

col1, col2 = st.columns(2)

# Shipping Cost by Ship Mode

with col1:

    fig = px.pie(
        ship_mode_summary,
        names="ship_mode",
        values="shipping_cost",
        hole=0.6,
        title="Shipping Cost Distribution"
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # Shipping Cost by Region

with col2:

    fig = px.bar(
        shipping_region,
        x="region",
        y="shipping_cost",
        color="shipping_cost",
        title="Regional Shipping Costs"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Order Priority Analysis

fig = px.bar(
    priority_summary,
    x="order_priority",
    y="sales",
    color="profit",
    title="Order Priority Performance"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)



# Logistics Efficiency Analysis 

ship_mode_summary["profit_per_shipping_dollar"] = (
    ship_mode_summary["profit"]
    /
    ship_mode_summary["shipping_cost"]
)


fig = px.bar(
    ship_mode_summary.sort_values(
        "profit_per_shipping_dollar",
        ascending=False
    ),
    x="ship_mode",
    y="profit_per_shipping_dollar",
    color="profit_per_shipping_dollar",
    title="Logistics Efficiency (Profit per Shipping Dollar)"
)

fig.update_layout(
    height=500,
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)




# Operational KPI Panel


best_ship_mode = (
    ship_mode_summary
    .sort_values("profit", ascending=False)
    .iloc[0]["ship_mode"]
)

highest_cost_region = (
    shipping_region
    .iloc[0]["region"]
)

best_priority = (
    priority_summary
    .sort_values("sales", ascending=False)
    .iloc[0]["order_priority"]
)


c1, c2, c3 = st.columns(3)

c1.success(
    f"""
    🚚 Best Shipping Method

    {best_ship_mode}
    """
)

c2.warning(
    f"""
    💸 Highest Cost Region

    {highest_cost_region}
    """
)

c3.info(
    f"""
    ⚡ Top Order Priority

    {best_priority}
    """
)


# Executive Operational Insights

st.markdown("### 🧠 Operational Intelligence Insights")

st.success(
    f"""
    ✔ {best_ship_mode} generates the highest profitability.

    ✔ {highest_cost_region} has the largest logistics cost burden.

    ✔ {best_priority} orders contribute the highest sales volume.

    ✔ Shipping efficiency varies significantly across regions.

    ✔ Logistics optimization can improve overall business margins.
    """
)


# Strategic Recommendations


st.markdown("### 🎯 Operations Strategy Recommendations")

st.info(
    f"""
    1. Expand use of high-efficiency shipping methods.

    2. Review logistics expenses in {highest_cost_region}.

    3. Optimize fulfillment processes for high-priority orders.

    4. Negotiate shipping contracts in expensive regions.

    5. Track shipping profitability alongside sales performance.
    """
)



