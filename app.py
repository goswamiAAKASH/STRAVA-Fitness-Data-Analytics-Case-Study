<<<<<<< HEAD
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

    # 1. Total Steps per User
    if analysis_option == "Total Steps per User":
        st.subheader("SQL Script")
        st.code("""SELECT Id, SUM(TotalSteps) AS TotalSteps
FROM cleaned_master
GROUP BY Id
ORDER BY TotalSteps DESC;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('Id')['TotalSteps'].sum().reset_index().sort_values(by='TotalSteps', ascending=False)""")

        result = df.groupby('Id')['TotalSteps'].sum().reset_index().sort_values(by='TotalSteps', ascending=False)
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        sns.barplot(x="Id", y="TotalSteps", data=result.head(10), ax=ax, palette="Blues_d")
        ax.set_title("Top Users by Total Steps")
        st.pyplot(fig)

    # 2. Average Calories per User
    elif analysis_option == "Average Calories per User":
        st.subheader("SQL Script")
        st.code("""SELECT Id, AVG(Calories) AS AvgCalories
FROM cleaned_master
GROUP BY Id
ORDER BY AvgCalories DESC;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('Id')['Calories'].mean().reset_index().sort_values(by='Calories', ascending=False)""")

        result = df.groupby('Id')['Calories'].mean().reset_index().sort_values(by='Calories', ascending=False)
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        sns.barplot(x="Id", y="Calories", data=result.head(10), ax=ax, palette="Oranges_d")
        ax.set_title("Top Users by Avg Calories")
        st.pyplot(fig)

    # 3. Top 5 Active Users
    elif analysis_option == "Top 5 Active Users":
        st.subheader("SQL Script")
        st.code("""SELECT Id, AVG(TotalSteps) AS AvgSteps
FROM cleaned_master
GROUP BY Id
ORDER BY AvgSteps DESC
LIMIT 5;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('Id')['TotalSteps'].mean().reset_index().sort_values(by='TotalSteps', ascending=False).head(5)""")

        result = df.groupby('Id')['TotalSteps'].mean().reset_index().sort_values(by='TotalSteps', ascending=False).head(5)
        st.dataframe(result)

        fig, ax = plt.subplots()
        sns.barplot(x="Id", y="TotalSteps", data=result, ax=ax, palette="Greens_d")
        ax.set_title("Top 5 Active Users by Avg Steps")
        st.pyplot(fig)

    # 4. Sleep Efficiency per User
    elif analysis_option == "Sleep Efficiency per User":
        st.subheader("SQL Script")
        st.code("""SELECT Id, AVG(TotalMinutesAsleep*1.0/TotalTimeInBed) AS SleepEfficiency
FROM cleaned_master
WHERE TotalTimeInBed > 0
GROUP BY Id;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.assign(Efficiency=df['TotalMinutesAsleep']/df['TotalTimeInBed']).groupby('Id')['Efficiency'].mean().reset_index()""")

        sleep_eff = df[df["TotalTimeInBed"] > 0].copy()
        sleep_eff["Efficiency"] = sleep_eff["TotalMinutesAsleep"] / sleep_eff["TotalTimeInBed"]
        result = sleep_eff.groupby("Id")["Efficiency"].mean().reset_index()
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        sns.boxplot(x="Efficiency", data=result, ax=ax, color="purple")
        ax.set_title("Sleep Efficiency Distribution")
        st.pyplot(fig)

    # 5. Daily Calories Trend
    elif analysis_option == "Daily Calories Trend":
        st.subheader("SQL Script")
        st.code("""SELECT ActivityDate, SUM(Calories) AS TotalCalories
FROM cleaned_master
GROUP BY ActivityDate
ORDER BY ActivityDate;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('ActivityDate')['Calories'].sum().reset_index().sort_values(by='ActivityDate')""")

        result = df.groupby("ActivityDate")["Calories"].sum().reset_index().sort_values(by="ActivityDate")
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        ax.plot(result["ActivityDate"], result["Calories"], marker="o", color="red")
        ax.set_title("Daily Calories Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Calories")
        st.pyplot(fig)

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

# -------------------------
# Downloads Page
# -------------------------
elif page == "Downloads":
    st.header("Downloads")
    st.download_button("Download Cleaned Dataset", df.to_csv(index=False).encode('utf-8'), "cleaned_master.csv")

    st.markdown("""
    ### Additional Files
    - [Download Project PPT](https://drive.google.com/file/d/your_ppt_id/view?usp=sharing)
    - [Download Full Report PDF](https://drive.google.com/file/d/your_pdf_id/view?usp=sharing)
    - [Download SQL Script](https://drive.google.com/file/d/your_sql_id/view?usp=sharing)
    """)
=======
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

    # 1. Total Steps per User
    if analysis_option == "Total Steps per User":
        st.subheader("SQL Script")
        st.code("""SELECT Id, SUM(TotalSteps) AS TotalSteps
FROM cleaned_master
GROUP BY Id
ORDER BY TotalSteps DESC;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('Id')['TotalSteps'].sum().reset_index().sort_values(by='TotalSteps', ascending=False)""")

        result = df.groupby('Id')['TotalSteps'].sum().reset_index().sort_values(by='TotalSteps', ascending=False)
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        sns.barplot(x="Id", y="TotalSteps", data=result.head(10), ax=ax, palette="Blues_d")
        ax.set_title("Top Users by Total Steps")
        st.pyplot(fig)

    # 2. Average Calories per User
    elif analysis_option == "Average Calories per User":
        st.subheader("SQL Script")
        st.code("""SELECT Id, AVG(Calories) AS AvgCalories
FROM cleaned_master
GROUP BY Id
ORDER BY AvgCalories DESC;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('Id')['Calories'].mean().reset_index().sort_values(by='Calories', ascending=False)""")

        result = df.groupby('Id')['Calories'].mean().reset_index().sort_values(by='Calories', ascending=False)
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        sns.barplot(x="Id", y="Calories", data=result.head(10), ax=ax, palette="Oranges_d")
        ax.set_title("Top Users by Avg Calories")
        st.pyplot(fig)

    # 3. Top 5 Active Users
    elif analysis_option == "Top 5 Active Users":
        st.subheader("SQL Script")
        st.code("""SELECT Id, AVG(TotalSteps) AS AvgSteps
FROM cleaned_master
GROUP BY Id
ORDER BY AvgSteps DESC
LIMIT 5;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('Id')['TotalSteps'].mean().reset_index().sort_values(by='TotalSteps', ascending=False).head(5)""")

        result = df.groupby('Id')['TotalSteps'].mean().reset_index().sort_values(by='TotalSteps', ascending=False).head(5)
        st.dataframe(result)

        fig, ax = plt.subplots()
        sns.barplot(x="Id", y="TotalSteps", data=result, ax=ax, palette="Greens_d")
        ax.set_title("Top 5 Active Users by Avg Steps")
        st.pyplot(fig)

    # 4. Sleep Efficiency per User
    elif analysis_option == "Sleep Efficiency per User":
        st.subheader("SQL Script")
        st.code("""SELECT Id, AVG(TotalMinutesAsleep*1.0/TotalTimeInBed) AS SleepEfficiency
FROM cleaned_master
WHERE TotalTimeInBed > 0
GROUP BY Id;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.assign(Efficiency=df['TotalMinutesAsleep']/df['TotalTimeInBed']).groupby('Id')['Efficiency'].mean().reset_index()""")

        sleep_eff = df[df["TotalTimeInBed"] > 0].copy()
        sleep_eff["Efficiency"] = sleep_eff["TotalMinutesAsleep"] / sleep_eff["TotalTimeInBed"]
        result = sleep_eff.groupby("Id")["Efficiency"].mean().reset_index()
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        sns.boxplot(x="Efficiency", data=result, ax=ax, color="purple")
        ax.set_title("Sleep Efficiency Distribution")
        st.pyplot(fig)

    # 5. Daily Calories Trend
    elif analysis_option == "Daily Calories Trend":
        st.subheader("SQL Script")
        st.code("""SELECT ActivityDate, SUM(Calories) AS TotalCalories
FROM cleaned_master
GROUP BY ActivityDate
ORDER BY ActivityDate;""", language="sql")

        st.subheader("Pandas Equivalent")
        st.code("""df.groupby('ActivityDate')['Calories'].sum().reset_index().sort_values(by='ActivityDate')""")

        result = df.groupby("ActivityDate")["Calories"].sum().reset_index().sort_values(by="ActivityDate")
        st.dataframe(result.head(10))

        fig, ax = plt.subplots()
        ax.plot(result["ActivityDate"], result["Calories"], marker="o", color="red")
        ax.set_title("Daily Calories Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Calories")
        st.pyplot(fig)

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

# -------------------------
# Downloads Page
# -------------------------
elif page == "Downloads":
    st.header("Downloads")
    st.download_button("Download Cleaned Dataset", df.to_csv(index=False).encode('utf-8'), "cleaned_master.csv")

    st.markdown("""
    ### Additional Files
    - [Download Project PPT](https://drive.google.com/file/d/your_ppt_id/view?usp=sharing)
    - [Download Full Report PDF](https://drive.google.com/file/d/your_pdf_id/view?usp=sharing)
    - [Download SQL Script](https://drive.google.com/file/d/your_sql_id/view?usp=sharing)
    """)
>>>>>>> 9a7b6f7223ac6451508a3ae03b51bf92873dadba
