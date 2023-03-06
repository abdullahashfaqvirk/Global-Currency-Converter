import streamlit as st
import requests
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image


# Get currency options

@st.cache_data
def get_currency_options():
    url = "https://api.exchangerate.host/symbols"
    response = requests.get(url)
    currency_data = response.json()
    return list(currency_data["symbols"].keys())


# Get conversion rate

@st.cache_data
def get_conversion_rate(base_currency, conversion_currency):
    url = f"https://api.exchangerate.host/convert?from={base_currency}&to={conversion_currency}"
    response = requests.get(url)
    if response.ok:
        conversion_rate_data = response.json()
        return conversion_rate_data["info"]["rate"]
    else:
        st.error("Failed to fetch conversion rate")
        st.stop()


# Get historical rates data

@st.cache_data
def get_historical_rates(base_currency, conversion_currency, start_date, end_date):
    url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base={base_currency}&symbols={conversion_currency}"
    response = requests.get(url)
    if response.ok:
        rates_data = response.json()
        rates = rates_data["rates"]
        rate_dates = []
        rate_values = []
        for date in rates:
            rate_dates.append(date)
            rate_values.append(rates[date][conversion_currency])
        data = {"date": rate_dates, "rate": rate_values}
        return pd.DataFrame(data)
    else:
        st.error("Failed to fetch historical rates data")
        st.stop()


def main():
    # Load the favicon and set up the page configuration
    favicon = Image.open('favicon.png')
    st.set_page_config(
        page_title="Global Currency Converter",
        page_icon=favicon,
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None
    )

    # Hide the Streamlit footer with CSS
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Setting up Title
    st.title("Global Currency Converter")

    # Sidebar - Input options
    st.sidebar.header("Input Options")

    # Get currency options
    currencies = get_currency_options()

    # Base currency
    base_currency = st.sidebar.selectbox(
        "Select base currency", currencies, index=currencies.index("USD"))

    # Conversion currency
    conversion_currency = st.sidebar.selectbox(
        "Select conversion currency", currencies, index=currencies.index("EUR"))

    # Currency conversion rates
    conversion_rate = get_conversion_rate(base_currency, conversion_currency)

    # Display current conversion rate
    st.write(f"1 {base_currency} is currently worth {conversion_rate} {conversion_currency}")

    # Section 1 - Currency Converter
    st.header("Currency Converter")

    # Amount to convert
    amount = st.number_input(
        f"Enter the amount of {base_currency} to convert", value=1.0)

    # Converted amount
    converted_amount = conversion_rate * amount
    st.write(f"{amount} {base_currency} is equal to {converted_amount} {conversion_currency}")

    # Section 2 - Historical Exchange Rates Visualization
    st.header("Historical Exchange Rates Visualization")

    # Get historical rates data
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    df = get_historical_rates(base_currency, conversion_currency, start_date, end_date)

    # Visualize data
    fig = px.line(df, x='date', y='rate', title=f"{base_currency} to {conversion_currency} exchange rates since {start_date}")
    fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=list([
        dict(count=7,
             label="1w",
             step="day",
             stepmode="backward"),
        dict(count=1,
             label="1m",
             step="month",
             stepmode="backward"),
        dict(count=6,
             label="6m",
             step="month",
             stepmode="backward"),
        dict(count=1,
             label="1y",
             step="year",
             stepmode="backward"),
        dict(step="all")
    ])))
    st.plotly_chart(fig)


main()
