# STRAVA / Bellabeat Fitness Data Analytics Case Study

This project analyzes fitness tracking data (steps, distance, calories, heart rate, sleep, and weight) using Python (Pandas + Streamlit), SQL, and Power BI. Multiple raw sources are combined into a single clean dataset (`cleaned_master.csv`) to support exploratory analysis, SQL insights, and interactive dashboarding.

## Highlights

- Streamlit app (`app.py`) for an end-to-end interactive experience:
  - Home overview
  - Exploratory Data Analysis with filters (User, Date range, Weekday)
  - SQL Insights (mirrors saved queries/results)
  - Embedded Power BI dashboard
  - Business recommendations and downloads
- Pandas notebook with charts (`4 Pandas Analysis/Pandas_analysis.ipynb`)
- SQL scripts for key metrics (`2 SQL Analysis/sql analysis/fitness_sql_analysis.sql`)
- Power BI report (`3 Power BI Analysis/power_bi_dashboard_analysis.pbix`) and online dashboard link

## Repository Structure

- `app.py` — Streamlit application that ties analysis and visuals together
- `cleaned_master.csv` — Unified dataset for analysis (≈943 rows, 22 columns)
- `requirements.txt` — Python dependencies (Streamlit, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, OpenPyXL, Plotly)
- `1/first.ipynb` — Data loading/exploration notebook (raw files overview)
- `4 Pandas Analysis/Pandas_analysis.ipynb` — EDA and visualizations in Pandas/Seaborn/Matplotlib
- `2 SQL Analysis/sql analysis/fitness_sql_analysis.sql` — SQL queries; results saved in `2 SQL Analysis/sql analysis/query result/`
- `3 Power BI Analysis/power_bi_dashboard_analysis.pbix` — Power BI report; PDFs in the same folder
- `STRAVA FITNESS APP.pptx`, `STRAVA Fitness Data Analytics Case Study.pdf` — Slides and report
- `power bi  link.txt` — Public Power BI dashboard link
- `dataset link.txt` — Duplicate link to the Power BI dashboard

## Dataset

Primary file: `cleaned_master.csv` with columns like:
- `Id`, `ActivityDate`, `TotalSteps`, `TotalDistance`, `TrackerDistance`
- `VeryActiveMinutes`, `FairlyActiveMinutes`, `LightlyActiveMinutes`, `SedentaryMinutes`
- `Calories`, `SleepDay`, `TotalSleepRecords`, `TotalMinutesAsleep`, `TotalTimeInBed`
- `Date` (weight timestamp), `WeightKg`, `BMI`

Notes:
- Sleep fields (`SleepDay`, `TotalMinutesAsleep`, `TotalTimeInBed`) are present for a subset of records.
- Some notebooks reference an absolute path (`D:\internship\proj 3\cleaned_master.csv`). If running locally, update those paths to the repo-relative `cleaned_master.csv`.

## Getting Started

1) Install Python dependencies:

```
pip install -r requirements.txt
```

2) Launch the Streamlit app:

```
streamlit run app.py
```

3) Open the app in your browser (Streamlit will print a local URL).

## Streamlit App Pages

- Home
  - Overview of goals and assets included in this case study.
- Exploratory Data Analysis
  - Filters: User selection (`Id`), date range (`ActivityDate`), and weekday filter.
  - Typical visuals: Average steps by user, sleep efficiency distribution, correlations between steps and calories, activity intensity breakdowns.
- SQL Insights
  - SQL-derived metrics shown alongside Pandas equivalents.
  - Saved CSV outputs available under `2 SQL Analysis/sql analysis/query result/`.
- Power BI Dashboard
  - Embedded report via public link (Power BI Service).
- Business Recommendations
  - Actionable ideas based on derived insights (sleep guidance, activity nudges, nutrition integration, weekly reports, targeted marketing).
- Downloads
  - Buttons and links for dataset and project artifacts (PPT, PDF, SQL script).

## SQL Analysis

SQL script: `2 SQL Analysis/sql analysis/fitness_sql_analysis.sql`

Key queries included:
- Average steps per user
- Sleep efficiency (`TotalMinutesAsleep / TotalTimeInBed`)
- Top 5 most active users (by `VeryActiveMinutes`)
- Average steps vs average calories
- Low activity but high sleep days (`TotalSteps < 5000 AND TotalMinutesAsleep > 400`)
- BMI distribution (average, min, max)

Saved results live in `2 SQL Analysis/sql analysis/query result/` (e.g. `1_Average Steps per User.csv`, `2_Sleep Efficiency.csv`, `3_Top 5 Most Active Users.csv`, `4_Average Steps vs Average Calories.csv`, `5_Low Activity but High Sleep Days.csv`, `6_BMI Distribution.csv`).

To run the SQL locally:
- Load `cleaned_master.csv` into your database as a table (e.g., `fitness_data`).
- Execute queries from `fitness_sql_analysis.sql` in your SQL engine (SQLite, PostgreSQL, etc.).
- Export results as needed to CSV for offline sharing.

## Power BI

- Desktop: Open `3 Power BI Analysis/power_bi_dashboard_analysis.pbix` in Power BI Desktop.
- Web: View the published dashboard:
  - https://app.powerbi.com/view?r=eyJrIjoiMTZkNjc2YjctMzFhMy00N2EwLThhNWEtMGFkZjU4ZTJmMzQ2IiwidCI6IjUyYTg3NmM3LTk2NzYtNGE4ZC04M2I1LTU3YjRmNDUyNGVkMSJ9

## Reproducibility & Tips

- Ensure `cleaned_master.csv` is present in the repo root before launching the app.
- If a notebook fails to read the dataset, update its path to the relative `cleaned_master.csv`.
- The Streamlit app caches data via `@st.cache_data` to improve performance.
- If you change the dataset, clear the Streamlit cache (from the app menu) and reload.

## Business Recommendations (Summary)

- Sleep wellness features: tracking, reminders, and relaxation guidance.
- Activity nudges: timely notifications during low-activity hours.
- Nutrition integration: align calorie analytics with food logging.
- Personalized weekly reports: progress tracking and insights.
- Targeted marketing: focus on evening exercisers and calorie-conscious users.

## Requirements

See `requirements.txt`. Typical stack:
- Streamlit, Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Scikit-learn, OpenPyXL

## Acknowledgements

- Fitbit/Bellabeat-style wearable datasets inspired by common case studies in analytics.
- Power BI dashboards created from the unified `cleaned_master.csv`.
