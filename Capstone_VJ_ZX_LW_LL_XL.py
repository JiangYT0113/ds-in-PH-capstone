import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Load COVID-19 data for deaths, cases, and recoveries
data_url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
data_url_cases = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
data_url_recoveries = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

data_deaths = pd.read_csv(data_url_deaths).drop(["Province/State", 'Lat', 'Long'], axis=1).groupby('Country/Region').sum().reset_index()
data_cases = pd.read_csv(data_url_cases).drop(["Province/State", 'Lat', 'Long'], axis=1).groupby('Country/Region').sum().reset_index()
data_recovery = pd.read_csv(data_url_recoveries).drop(["Province/State", 'Lat', 'Long'], axis=1).groupby('Country/Region').sum().reset_index()

# Webpage design
st.title("COVID-19 Dashboard")
st.caption("Team Members: Vicky Jiang, Zijun Xie, Lijie Wu, Liyuan Liu, Xintong Li")

# Select country
selected_country = st.selectbox("Select a country", data_deaths['Country/Region'].unique())

# Radio buttons to select which figure to display
figure_option = st.radio(
    "Choose a figure to display",
    ('Daily Cases', 'Daily Deaths', 'Daily Recoveries', 'Detailed Data Table')
)

# Define a function to get the daily data for a specific metric
def get_country_data(country_name, data, drop_columns):
    y = data[data['Country/Region'] == country_name].drop(["Country/Region"], axis=1).sum()
    y = np.asarray(y)
    daily_changes = y[1:] - y[:-1]
    daily_changes = np.clip(daily_changes, 0, None)
    first_non_zero_index = np.argmax(daily_changes > 0) if daily_changes.any() else 0
    y = daily_changes[first_non_zero_index:]
    return y

# Get data
y_deaths = get_country_data(selected_country, data_deaths, ["Province/State", "Country/Region", "Lat", "Long"])
y_cases = get_country_data(selected_country, data_cases, ["Province/State", "Country/Region", "Lat", "Long"])
y_recoveries = get_country_data(selected_country, data_recovery, ["Province/State", "Country/Region", "Lat", "Long"])

# Dates for x-axis
start_date = pd.to_datetime('2020-01-22')
dates = pd.date_range(start_date, periods=max(len(y_cases), len(y_deaths), len(y_recoveries)))

def plot_figure(data, title):
    fig = px.line(
        x=dates[:len(data)],
        y=data,
        labels={'x': 'Date', 'y': title},
        title=f'{title} in {selected_country}'
    )
    return fig

# Define a function for detailed data table
def get_country_timeseries(df, country_name):
    return df[df['Country/Region'] == country_name].drop('Country/Region', axis=1).iloc[0]

def calculate_daily_change(timeseries):
    return np.diff(timeseries, prepend=timeseries.iloc[0])

# Get the timeseries data for the selected country
cases_timeseries = get_country_timeseries(data_cases, selected_country)
deaths_timeseries = get_country_timeseries(data_deaths, selected_country)
recovery_timeseries = get_country_timeseries(data_recovery, selected_country)

# Calculate the daily changes
cases_y = calculate_daily_change(cases_timeseries)
deaths_y = calculate_daily_change(deaths_timeseries)
recoveries_y = calculate_daily_change(recovery_timeseries)

# Create a date range for the length of the data
dates = pd.date_range(start=start_date, periods=len(cases_timeseries))

# Prepare the combined DataFrame
combined_df = pd.DataFrame({
    'Date': dates,
    'Cases': cases_y,
    'Deaths': deaths_y,
    'Recoveries': recoveries_y
})

# Show the selected figure
if figure_option == 'Daily Cases':
    fig_cases = plot_figure(y_cases, 'Daily Cases')
    st.plotly_chart(fig_cases, use_container_width=True)
elif figure_option == 'Daily Deaths':
    fig_deaths = plot_figure(y_deaths, 'Daily Deaths')
    st.plotly_chart(fig_deaths, use_container_width=True)
elif figure_option == 'Daily Recoveries':
    fig_recoveries = plot_figure(y_recoveries, 'Daily Recoveries')
    st.plotly_chart(fig_recoveries, use_container_width=True)
elif figure_option == 'Detailed Data Table':
    st.subheader(f"COVID-19 Daily Changes for {selected_country}")
    st.table(combined_df.set_index('Date'))
