import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# PAGE CONFIGURATION


st.set_page_config(
    page_title="Global Tech Startups 2026 Analytics Dashboard",
    layout="wide"
)


# LOAD DATA


@st.cache_data
def load_data():

    df = pd.read_csv("cleaned_startups.csv")

    return df


df = load_data()

# TITLE


st.title("Global Tech Startups 2026 Analytics Dashboard")

st.markdown(
    """
    ### Global Startup Analytics
    Analyze funding, valuation, revenue, workforce,
    AI adoption and startup risk.
    """
)

st.divider()


# SIDEBAR FILTERS


st.sidebar.header("Filters")

# Domain
domains = st.sidebar.multiselect(
    "Technology Domain",
    options=sorted(df["Domain"].unique()),
    default=sorted(df["Domain"].unique())
)

# Country
countries = st.sidebar.multiselect(
    "Country",
    options=sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

# Funding Stage
funding_stages = st.sidebar.multiselect(
    "Funding Stage",
    options=sorted(df["Funding_Stage"].unique()),
    default=sorted(df["Funding_Stage"].unique())
)

# Investor Tier
investor_tiers = st.sidebar.multiselect(
    "Investor Tier",
    options=sorted(df["Investor_Tier"].unique()),
    default=sorted(df["Investor_Tier"].unique())
)

# AI Adoption
ai_levels = st.sidebar.multiselect(
    "AI Adoption",
    options=sorted(df["AI_Adoption_Level"].unique()),
    default=sorted(df["AI_Adoption_Level"].unique())
)

# Acquisition status
acquisition_status = st.sidebar.multiselect(
    "Acquisition Status",
    options=sorted(df["Acquisition_Status"].unique()),
    default=sorted(df["Acquisition_Status"].unique())
)


# APPLY FILTERS


filtered_df = df[
    df["Domain"].isin(domains)
    & df["Country"].isin(countries)
    & df["Funding_Stage"].isin(funding_stages)
    & df["Investor_Tier"].isin(investor_tiers)
    & df["AI_Adoption_Level"].isin(ai_levels)
    & df["Acquisition_Status"].isin(acquisition_status)
]


# KPI CALCULATIONS


total_startups = len(filtered_df)

total_funding = filtered_df[
    "Total_Funding_USD_Millions"
].sum()

total_valuation = filtered_df[
    "Valuation_USD_Millions"
].sum()

total_revenue = filtered_df[
    "Revenue_ARR_Millions"
].sum()

average_runway = filtered_df[
    "Runway_Months_2024"
].mean()

total_employees = filtered_df[
    "Current_Headcount_2026"
].sum()


# KPI CARDS


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Startups",
    f"{total_startups:,}"
)

col2.metric(
    "Total Funding",
    f"${total_funding:,.1f} M"
)

col3.metric(
    "Total Valuation",
    f"${total_valuation:,.1f} M"
)

col4.metric(
    "Total Revenue",
    f"${total_revenue:,.1f} M"
)

col5, col6, col7 = st.columns(3)

col5.metric(
    "Avg Runway",
    f"{average_runway:f} Months"
)

col6.metric(
    "Employees",
    f"{total_employees:,}"
)

col7.metric(
    "High Risk Startups",
    f"{(filtered_df['Risk_Category'] == 'High Risk').sum():,}"
)

st.divider()


# CHART 1 - STARTUPS BY DOMAIN


st.subheader("Startup Distribution by Technology Domain")

domain_count = (
    filtered_df["Domain"]
    .value_counts()
    .reset_index()
)

domain_count.columns = ["Domain", "Startups"]

fig_domain = px.bar(
    domain_count,
    x="Domain",
    y="Startups",
    title="Number of Startups by Domain"
)

st.plotly_chart(
    fig_domain,
    use_container_width=True
)


# CHART 2 - FUNDING BY DOMAIN


st.subheader("Funding by Technology Domain")

funding_domain = (
    filtered_df.groupby("Domain")[
        "Total_Funding_USD_Millions"
    ]
    .sum()
    .reset_index()
    .sort_values(
        "Total_Funding_USD_Millions",
        ascending=False
    )
)

fig_funding = px.bar(
    funding_domain,
    x="Domain",
    y="Total_Funding_USD_Millions",
    title="Total Funding by Domain"
)

st.plotly_chart(
    fig_funding,
    use_container_width=True
)


# CHART 3 - FUNDING STAGE


st.subheader("Funding Stage Analysis")

stage_data = (
    filtered_df.groupby("Funding_Stage")
    .agg(
        Startups=("Company_ID", "count"),
        Funding=("Total_Funding_USD_Millions", "sum"),
        Valuation=("Valuation_USD_Millions", "sum")
    )
    .reset_index()
)

fig_stage = px.bar(
    stage_data,
    x="Funding_Stage",
    y="Funding",
    title="Funding by Funding Stage",
    text_auto=".2s"
)

st.plotly_chart(
    fig_stage,
    use_container_width=True
)


# CHART 4 - COUNTRY


st.subheader("Startup Distribution by Country")

country_data = (
    filtered_df["Country"]
    .value_counts()
    .reset_index()
)

country_data.columns = [
    "Country",
    "Startups"
]

fig_country = px.pie(
    country_data,
    names="Country",
    values="Startups",
    title="Startups by Country"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

# CHART 5 - REVENUE VS FUNDING


st.subheader("Revenue vs Funding")

fig_scatter = px.scatter(
    filtered_df,
    x="Total_Funding_USD_Millions",
    y="Revenue_ARR_Millions",
    size="Valuation_USD_Millions",
    color="Domain",
    hover_name="Company_ID",
    title="Revenue vs Total Funding"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# CHART 6 - AI ADOPTION


st.subheader("AI Adoption Analysis")

ai_data = (
    filtered_df["AI_Adoption_Level"]
    .value_counts()
    .reset_index()
)

ai_data.columns = [
    "AI_Adoption_Level",
    "Startups"
]

fig_ai = px.bar(
    ai_data,
    x="AI_Adoption_Level",
    y="Startups",
    title="AI Adoption Level"
)

st.plotly_chart(
    fig_ai,
    use_container_width=True
)


# CHART 7 - AI BY DOMAIN


ai_domain = pd.crosstab(
    filtered_df["Domain"],
    filtered_df["AI_Adoption_Level"]
).reset_index()

ai_domain_long = ai_domain.melt(
    id_vars="Domain",
    var_name="AI Adoption",
    value_name="Startups"
)

fig_ai_domain = px.bar(
    ai_domain_long,
    x="Domain",
    y="Startups",
    color="AI Adoption",
    barmode="group",
    title="AI Adoption by Technology Domain"
)

st.plotly_chart(
    fig_ai_domain,
    use_container_width=True
)


# WORKFORCE ANALYSIS


st.subheader("Workforce Analysis")

workforce = (
    filtered_df.groupby("Domain")
    .agg(
        Peak_Headcount=(
            "Peak_Headcount_2023",
            "sum"
        ),
        Current_Headcount=(
            "Current_Headcount_2026",
            "sum"
        ),
        Layoffs=(
            "Layoffs_2024_2025",
            "sum"
        )
    )
    .reset_index()
)

workforce_long = workforce.melt(
    id_vars="Domain",
    value_vars=[
        "Peak_Headcount",
        "Current_Headcount",
        "Layoffs"
    ],
    var_name="Metric",
    value_name="Employees"
)

fig_workforce = px.bar(
    workforce_long,
    x="Domain",
    y="Employees",
    color="Metric",
    barmode="group",
    title="Workforce and Layoffs by Domain"
)

st.plotly_chart(
    fig_workforce,
    use_container_width=True
)


# RISK ANALYSIS


st.subheader("Startup Risk Analysis")

risk_data = (
    filtered_df["Risk_Category"]
    .value_counts()
    .reset_index()
)

risk_data.columns = [
    "Risk Category",
    "Startups"
]

fig_risk = px.pie(
    risk_data,
    names="Risk Category",
    values="Startups",
    title="Startup Risk Distribution"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# TOP STARTUPS


st.subheader("Top Startups by Valuation")

top_startups = (
    filtered_df[
        [
            "Company_ID",
            "Domain",
            "Country",
            "Funding_Stage",
            "Total_Funding_USD_Millions",
            "Valuation_USD_Millions",
            "Revenue_ARR_Millions",
            "Runway_Months_2024",
            "AI_Adoption_Level",
            "Risk_Category"
        ]
    ]
    .sort_values(
        "Valuation_USD_Millions",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_startups,
    use_container_width=True
)


# DOWNLOAD DATA


st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_startups.csv",
    mime="text/csv"
)


# FOOTER


st.divider()

st.caption(
    "Global Tech Startups 2026 | "
    "Python + Pandas + Plotly + Streamlit"
)