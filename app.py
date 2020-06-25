import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

def main():
    st.title("COVID-19 Data Analysis 🦠")
    st.sidebar.title("COVID-19 Data Analysis 🦠")
    st.subheader("By Richard Cornelius Suwandi")
    st.sidebar.markdown("By Richard Cornelius Suwandi")
    st.markdown(
        "Time series visualizations on the number of confirmed cases,\
        deaths, and recoveries from COVID-19. \
        between 22 January 2020 to 22 June 2020."
        )

    @st.cache(persist=True)
    def load_data(filename):
        data = pd.read_csv(filename)
        data.drop(["Lat", "Long"], axis=1, inplace=True)
        return data

    covid_confirmed = load_data("covid_confirmed.csv")
    covid_deaths = load_data("covid_deaths.csv")
    covid_recovered = load_data("covid_confirmed.csv")

    covid_confirmed_agg = covid_confirmed.groupby("Country/Region").sum()
    covid_deaths_agg = covid_deaths.groupby("Country/Region").sum()
    covid_recovered_agg = covid_recovered.groupby("Country/Region").sum()

    covid_data_dict = {
        "Confirmed Cases": [covid_confirmed_agg, "Infection Rate"] ,
        "Death Cases": [covid_deaths_agg, "Death Rate"],
        "Recovered Cases": [covid_recovered_agg, "Recovery Rate"]
        }

    choice = st.sidebar.radio("Which data to plot?", ("Confirmed Cases", "Death Cases", "Recovered Cases"))
    covid_data = covid_data_dict[choice][0]

    # Plot by country/countries
    countries = st.sidebar.multiselect("Choose the country/region to plot", tuple(covid_data.index))

    # Plot by month
    month = st.sidebar.radio("Choose a specific month to plot", ("January", "February",  "March", "April", "May", "June", "All Months"))

    months_dict = {
        "January": (0, 10),
        "February": (10, 39),
        "March": (39, 70),
        "April": (70, 100),
        "May": (100, 131),
        "June": (131, 153)
    }

    if month == "All Months":
        days = st.sidebar.slider('How many days do you want to plot?', 5, len(covid_data.columns))
        if len(countries) > 0:
            for country in countries:
                covid_data.loc[country][:days].plot(label=country)
            plt.xlabel("Date")
            plt.ylabel(f"Number of {choice}")
            plt.title(f"Number of {choice} by Date")
            plt.legend()
            st.pyplot()

            for country in countries:
                covid_data.loc[country][:days].diff().plot(label=country)
            plt.xlabel("Date")
            plt.ylabel(covid_data_dict[choice][1])
            plt.title(f"{covid_data_dict[choice][1]} by Date")
            plt.legend()
            st.pyplot()

    else:
        if len(countries) > 0:
            for country in countries:
                start, end = months_dict[month]
                covid_data.loc[country][start:end].plot(label=country)
            plt.xlabel("Date")
            plt.ylabel(f"Number of {choice}")
            plt.title(f"Number of {choice} in {month}")
            plt.legend()
            st.pyplot()

            for country in countries:
                start, end = months_dict[month]
                covid_data.loc[country][start:end].diff().plot(label=country)
            plt.xlabel("Date")
            plt.ylabel(covid_data_dict[choice][1])
            plt.title(f"{covid_data_dict[choice][1]} in {month}")
            plt.legend()
            st.pyplot()

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader(f"COVID-19 Data for {len(covid_data)} Countries/Regions")
        st.write(covid_data)

if __name__ == "__main__":
    main()
