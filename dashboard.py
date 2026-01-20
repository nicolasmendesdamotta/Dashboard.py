import streamlit as st
import pandas as pd
import plotly.express as px
import locale

locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

st.set_page_config(layout='wide')

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

# Convert date column (accepting mixed formats)
df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True)

# Sort by date
df = df.sort_values("Date")

# Create month column
df["Month"] = df["Date"].dt.strftime("%b/%Y")

# ==================================================
# NEW: Create a numerical month key to allow comparison
# (This helps us calculate Month-over-Month Growth)
# ==================================================
df["Month_Key"] = df["Date"].dt.to_period("M")

# ---- SIDEBAR ----
month = st.sidebar.selectbox("Select Month", df["Month"].unique())

# ---- MAIN CONTENT ----
st.title("Sales Dashboard")
st.subheader(f"Data for: {month}")

# Filter data by selected month
df_filtrado = df[df["Month"] == month]

# ==================================================
# NEW: Calculate PREVIOUS month data for growth KPI
# ==================================================
current_month_key = df_filtrado["Month_Key"].iloc[0]
prev_month_key = current_month_key - 1  # Previous month

df_prev = df[df["Month_Key"] == prev_month_key]

# ---- KPIs IN A ROW (NOW 5 KPIs) ----
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_revenue = df_filtrado["Total"].sum()
avg_rating = df_filtrado["Rating"].mean()
top_city = df_filtrado.groupby("City")["Total"].sum().idxmax()
top_payment = df_filtrado["Payment"].mode()[0]
top_product = (
    df_filtrado.groupby("Product line")["Total"]
    .sum()
    .idxmax()
)

# NEW: Month-over-Month Growth Calculation
prev_revenue = df_prev["Total"].sum() if not df_prev.empty else None

if prev_revenue and prev_revenue > 0:
    revenue_growth = ((total_revenue - prev_revenue) / prev_revenue) * 100
    growth_text = f"{revenue_growth:+.1f}%"
else:
    growth_text = "N/A"

kpi1.metric("Total Revenue (Month)", f"R$ {total_revenue:,.2f}")
kpi2.metric("Customer Satisfaction (0–10)", round(avg_rating, 2))
kpi3.metric("Top Performing City", top_city)
kpi4.metric("Most Used Payment", top_payment)
kpi5.metric("MoM Revenue Growth", growth_text)

# ---- TABS FOR CITIES ----
tab_all, tab_yangon, tab_naypyitaw, tab_mandalay = st.tabs(
    ["All Cities", "Yangon", "Naypyitaw", "Mandalay"]
)

# ==================================================
# ALL CITIES TAB
# ==================================================
with tab_all:
    st.subheader("Overview: All Cities")

    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)

    # Daily Revenue (Bar Chart)
    fig_date = px.bar(
        df_filtrado,
        x="Date",
        y="Total",
        color="City",
        title="Daily Revenue"
    )
    col1.plotly_chart(fig_date, use_container_width=True, key="daily_all")

    # Revenue by Product Line
    prod_total = (
        df_filtrado
        .groupby("Product line")["Total"]
        .sum()
        .reset_index()
    )

    fig_prod = px.bar(
        prod_total,
        x="Total",
        y="Product line",
        orientation='h',
        title="Revenue by Product Line"
    )
    col2.plotly_chart(fig_prod, use_container_width=True, key="prod_all")

    # Total revenue by branch
    city_total = (
        df_filtrado
        .groupby("City")["Total"]
        .sum()
        .reset_index()
    )

    fig_city = px.bar(
        city_total,
        x="City",
        y="Total",
        title="Total Revenue by Branch"
    )
    col3.plotly_chart(fig_city, use_container_width=True, key="city_all")

    # Payment method distribution (ALL CITIES)
    fig_method = px.pie(
        df_filtrado,
        values="Total",
        names="Payment",
        title="Revenue by Payment Method"
    )
    col4.plotly_chart(fig_method, use_container_width=True, key="pay_all")

    # Average rating by branch
    fig_rating = px.bar(
        df_filtrado,
        y="Rating",
        x="City",
        title="Customer Rating by Branch"
    )
    col5.plotly_chart(fig_rating, use_container_width=True, key="rating_all")

# ==================================================
# YANGON TAB
# ==================================================
with tab_yangon:
    st.subheader("Yangon Performance")

    df_yangon = df_filtrado[df_filtrado["City"] == "Yangon"]

    col1, col2, col3 = st.columns(3)

    fig_yangon = px.bar(
        df_yangon,
        x="Date",
        y="Total",
        title="Daily Revenue - Yangon"
    )
    col1.plotly_chart(fig_yangon, use_container_width=True, key="daily_yangon")

    fig_yangon_prod = px.bar(
        df_yangon.groupby("Product line")["Total"].sum().reset_index(),
        x="Total",
        y="Product line",
        orientation='h',
        title="Revenue by Product Line - Yangon"
    )
    col2.plotly_chart(fig_yangon_prod, use_container_width=True, key="prod_yangon")

    fig_yangon_pay = px.pie(
        df_yangon,
        values="Total",
        names="Payment",
        title="Payment Method - Yangon"
    )
    col3.plotly_chart(fig_yangon_pay, use_container_width=True, key="pay_yangon")

# ==================================================
# NAYPYITAW TAB
# ==================================================
with tab_naypyitaw:
    st.subheader("Naypyitaw Performance")

    df_nay = df_filtrado[df_filtrado["City"] == "Naypyitaw"]

    col1, col2, col3 = st.columns(3)

    fig_nay = px.bar(
        df_nay,
        x="Date",
        y="Total",
        title="Daily Revenue - Naypyitaw"
    )
    col1.plotly_chart(fig_nay, use_container_width=True, key="daily_nay")

    fig_nay_prod = px.bar(
        df_nay.groupby("Product line")["Total"].sum().reset_index(),
        x="Total",
        y="Product line",
        orientation='h',
        title="Revenue by Product Line - Naypyitaw"
    )
    col2.plotly_chart(fig_nay_prod, use_container_width=True, key="prod_nay")

    fig_nay_pay = px.pie(
        df_nay,
        values="Total",
        names="Payment",
        title="Payment Method - Naypyitaw"
    )
    col3.plotly_chart(fig_nay_pay, use_container_width=True, key="pay_nay")

# ==================================================
# MANDALAY TAB
# ==================================================
with tab_mandalay:
    st.subheader("Mandalay Performance")

    df_mandalay = df_filtrado[df_filtrado["City"] == "Mandalay"]

    col1, col2, col3 = st.columns(3)

    fig_man = px.bar(
        df_mandalay,
        x="Date",
        y="Total",
        title="Daily Revenue - Mandalay"
    )
    col1.plotly_chart(fig_man, use_container_width=True, key="daily_mandalay")

    fig_man_prod = px.bar(
        df_mandalay.groupby("Product line")["Total"].sum().reset_index(),
        x="Total",
        y="Product line",
        orientation='h',
        title="Revenue by Product Line - Mandalay"
    )
    col2.plotly_chart(fig_man_prod, use_container_width=True, key="prod_mandalay")

    fig_man_pay = px.pie(
        df_mandalay,
        values="Total",
        names="Payment",
        title="Payment Method - Mandalay"
    )
    col3.plotly_chart(fig_man_pay, use_container_width=True, key="pay_mandalay")
