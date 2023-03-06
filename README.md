# Global-Currency-Converter

This is a Python script that utilizes Streamlit, requests, pandas, datetime, plotly and PIL libraries to create a global currency converter with an exchange rate visualization.

## Installation

Install the required libraries: ```pip install -r requirements.txt```   


## Usage

Run the script using this command: ```streamlit run currency_converter.py```

Once you run the script, you will see a web page with the title "Global Currency Converter" and two sections: "Currency Converter" and "Historical Exchange Rates Visualization".    

In the "Currency Converter" section, you can select a base currency and a conversion currency from the dropdown menus. The script will display the current conversion rate and allow you to enter an amount of the base currency to convert. The script will then calculate and display the converted amount.      
  
In the "Historical Exchange Rates Visualization" section, the script will fetch the historical exchange rates between the selected base and conversion currencies for the past year and display them as a line chart. You can use the range selector to zoom in on a specific time period.       
