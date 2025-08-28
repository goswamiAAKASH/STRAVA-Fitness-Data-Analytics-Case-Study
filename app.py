import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Load Dataset
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_master.csv", parse_dates=["ActivityDate"])
    return df

df = load_data()

# -------------------------
# App Layout
# -------------------------
st.set_page_config(page_title="Strava Fitness Analytics", layout="wide")
st.title("Strava / Bellabeat Fitness Analytics Dashboard")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Exploratory Data Analysis",
    "SQL Insights",
    "Power BI Dashboard",
    "Business Recommendations",
    "Downloads"
])

# -------------------------
# Home Page
# -------------------------
if page == "Home":
    st.subheader("Welcome to the Strava / Bellabeat Fitness Analysis Web App")
    st.markdown("""
    This application showcases data analysis from Fitbit/Strava datasets including:
    - Exploratory Data Analysis (EDA)
    - SQL-based insights with Pandas equivalents
    - Power BI interactive dashboard
    - Business recommendations
    - Downloads of reports, PPTs, and cleaned dataset
    """)

# -------------------------
# EDA Page
# -------------------------
elif page == "Exploratory Data Analysis":
    st.header("Exploratory Data Analysis")

    # Sidebar filters for analysis
    st.sidebar.header("Filters")
    user_ids = st.sidebar.multiselect("Select User(s)", options=df["Id"].unique())
    date_range = st.sidebar.date_input("Select Date Range", [df["ActivityDate"].min(), df["ActivityDate"].max()])
    weekday_filter = st.sidebar.multiselect("Select Weekdays", options=list(df["ActivityDate"].dt.day_name().unique()))

    filtered_df = df.copy()
    if user_ids:
        filtered_df = filtered_df[filtered_df["Id"].isin(user_ids)]
    if isinstance(date_range, list) and len(date_range) == 2:
        filtered_df = filtered_df[(filtered_df["ActivityDate"] >= pd.to_datetime(date_range[0])) & (filtered_df["ActivityDate"] <= pd.to_datetime(date_range[1]))]
    if weekday_filter:
        filtered_df = filtered_df[filtered_df["ActivityDate"].dt.day_name().isin(weekday_filter)]

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Steps", int(filtered_df["TotalSteps"].mean()))
    with col2:
        st.metric("Avg Calories", int(filtered_df["Calories"].mean()))
    with col3:
        if "TotalMinutesAsleep" in filtered_df and filtered_df["TotalMinutesAsleep"].notna().sum() > 0:
            st.metric("Avg Sleep (hrs)", round(filtered_df["TotalMinutesAsleep"].mean() / 60, 1))
        else:
            st.metric("Avg Sleep (hrs)", "N/A")
    with col4:
        if "TotalMinutesAsleep" in filtered_df and "TotalTimeInBed" in filtered_df and filtered_df["TotalTimeInBed"].notna().sum() > 0:
            eff = filtered_df["TotalMinutesAsleep"].sum() / filtered_df["TotalTimeInBed"].sum()
            st.metric("Sleep Efficiency %", round(eff * 100, 1))
        else:
            st.metric("Sleep Efficiency %", "N/A")

    # Charts
    st.subheader("Visualizations")

    # Steps vs Calories Scatter
    fig, ax = plt.subplots()
    sns.scatterplot(x="TotalSteps", y="Calories", data=filtered_df, alpha=0.6, ax=ax)
    ax.set_title("Steps vs Calories")
    st.pyplot(fig)

    # Avg Steps by Weekday
    fig, ax = plt.subplots()
    weekday_steps = filtered_df.copy()
    weekday_steps["Weekday"] = weekday_steps["ActivityDate"].dt.day_name()
    weekday_avg = weekday_steps.groupby("Weekday")["TotalSteps"].mean().reindex(
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    weekday_avg.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Average Steps by Weekday")
    ax.set_ylabel("Steps")
    st.pyplot(fig)

    # Calories Distribution
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["Calories"], bins=30, kde=True, ax=ax, color="orange")
    ax.set_title("Calories Distribution")
    st.pyplot(fig)

# -------------------------
# SQL Insights Page
# -------------------------
elif page == "SQL Insights":
    st.header("SQL Insights with Pandas Equivalent")

    analysis_option = st.selectbox(
        "Choose Analysis",
        [
            "Total Steps per User",
            "Average Calories per User",
            "Top 5 Active Users",
            "Sleep Efficiency per User",
            "Daily Calories Trend"
        ]
    )

    # (SQL + Pandas Analysis as in your original code)
    # ... keep the same logic here ...

# -------------------------
# Power BI Page
# -------------------------
elif page == "Power BI Dashboard":
    st.header("Interactive Power BI Dashboard")
    st.components.v1.iframe(
        src="https://app.powerbi.com/view?r=eyJrIjoiMTZkNjc2YjctMzFhMy00N2EwLThhNWEtMGFkZjU4ZTJmMzQ2IiwidCI6IjUyYTg3NmM3LTk2NzYtNGE4ZC04M2I1LTU3YjRmNDUyNGVkMSJ9",
        width=1200,
        height=600
    )

# -------------------------
# Recommendations Page
# -------------------------
elif page == "Business Recommendations":
    st.header("Business Recommendations for Bellabeat")
    st.markdown("""
    1. Sleep Wellness Features → Promote sleep tracking, bedtime reminders, and relaxation guidance.
    2. Activity Nudges → Send notifications during low-activity hours (afternoons, weekdays).
    3. Nutrition Integration → Combine calorie tracking with food logs.
    4. Personalized Reports → Weekly health reports for users to track progress.
    5. Targeted Marketing → Focus campaigns on evening exercisers and calorie-conscious users.
    """)

# Downloads Page

elif page == "Downloads":
    st.header("Downloads")
    st.download_button("Download Cleaned Dataset", df.to_csv(index=False).encode('utf-8'), "cleaned_master.csv")

    st.markdown("""
    ### Additional Files
    - [Download Project PPT](https://drive.google.com/uc?export=download&id=1HBI_d4WlyiN6QKV91-HxWzxw_nWZImQB)
    - [Download Full Report PDF](https://drive.google.com/uc?export=download&id=1KulkBp38vZfp7ME4dE9xQTGe-jqDQlTT)
    - [Download SQL Script](https://drive.google.com/uc?export=download&id=1WVyrK34p2BVbfhT0fx5KC2hKdpaGmnfX)
    """)
