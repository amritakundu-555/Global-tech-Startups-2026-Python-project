import pandas as pd
import numpy as np

df = pd.read_csv("global_tech_startups_2026.csv")

print(df.shape)

print(df.columns)

print(df.isnull().sum())


missing_percentage = df.isnull().mean() * 100

print(missing_percentage)


df["AI_Adoption_Level"] = df["AI_Adoption_Level"].fillna("Unknown")

duplicates = df[df.duplicated("Company_ID", keep=False)]

print(duplicates)


print(
    df[df["Company_ID"].duplicated(keep=False)]
    .sort_values("Company_ID")
)


df = df.drop_duplicates(subset="Company_ID", keep="first")


numeric_columns = [
    "Founding_Year",
    "Total_Funding_USD_Millions",
    "Valuation_USD_Millions",
    "Revenue_ARR_Millions",
    "Monthly_Burn_Rate_Millions",
    "Runway_Months_2024",
    "Peak_Headcount_2023",
    "Layoffs_2024_2025",
    "Current_Headcount_2026"
]

print(df[numeric_columns].describe())


positive_columns = [
    "Total_Funding_USD_Millions",
    "Valuation_USD_Millions",
    "Revenue_ARR_Millions",
    "Monthly_Burn_Rate_Millions",
    "Runway_Months_2024",
    "Peak_Headcount_2023",
    "Layoffs_2024_2025",
    "Current_Headcount_2026"
]

for col in positive_columns:
    print(col, (df[col] < 0).sum())


    df["Company_Age_2026"] = 2026 - df["Founding_Year"]


    df["Revenue_Funding_Ratio"] = (
    df["Revenue_ARR_Millions"] /
    df["Total_Funding_USD_Millions"].replace(0, pd.NA)
)


    df["Layoff_Percentage"] = (
    df["Layoffs_2024_2025"] /
    df["Peak_Headcount_2023"].replace(0, pd.NA)
) * 100


    #headcount change
    df["Headcount_Change"] = (
    df["Current_Headcount_2026"] -
    df["Peak_Headcount_2023"]
)

    #headcount retation

    df["Headcount_Retention_Percentage"] = (
    df["Current_Headcount_2026"] /
    df["Peak_Headcount_2023"].replace(0, pd.NA)
) * 100


# Clean column names
df.columns = df.columns.str.strip()

# Calculate Layoff Percentage
df["Layoff_Percentage"] = (
    df["Layoffs_2024_2025"] /
    df["Peak_Headcount_2023"].replace(0, np.nan)
) * 100


# Create Risk Category
def risk_category(row):

    if row["Runway_Months_2024"] < 6 and row["Layoff_Percentage"] > 20:
        return "High Risk"

    elif row["Runway_Months_2024"] < 12 or row["Layoff_Percentage"] > 10:
        return "Medium Risk"

    else:
        return "Low Risk"


df["Risk_Category"] = df.apply(risk_category, axis=1)


# Check result
print(df[[
    "Company_ID",
    "Runway_Months_2024",
    "Layoff_Percentage",
    "Risk_Category"
]].head(20))



df.to_csv("cleaned_startups.csv", index=False)

print("Data cleaning completed.")
print("Rows:", len(df))
print("Columns:", len(df.columns))