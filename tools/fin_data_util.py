import pandas as pd
import requests
from api_util import get_api_key


def query_api(api_url, params):
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed: Status code = {response.status_code}")
    return response.json()


def get_twse_data(stock_id, date):
    api_url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"
    params = {"stockNo": str(stock_id), "date": date.strftime("%Y%m%d"), "response": "json"}
    return query_api(api_url, params)


def process_twse_response(data):
    # date = data["date"]
    cols = data["fields"]
    data = data["data"]
    return pd.DataFrame(data, columns=cols).applymap(lambda x: x.strip())


def get_twelve_data_stock_data(symbol, interval):
    api_key = get_api_key("TWELVE_DATA_KEY")
    api_url = "https://api.twelvedata.com/time_series"

    params = {"symbol": symbol, "interval": interval, "apikey": api_key}

    return query_api(api_url, params)


def get_alpha_vantage_stock_data(symbol, interval):
    api_key = get_api_key("ALPHA_VANTAGE_KEY")
    api_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_INTRADAY_EXTENDED" if interval == "1min" else "TIME_SERIES_INTRADAY"

    params = {"function": function, "symbol": symbol, "exchange": "TWSE", "interval": interval, "apikey": api_key}

    return query_api(api_url, params)


def get_alpha_vantage_fx_data(from_currency, to_currency):
    api_key = get_api_key("ALPHA_VANTAGE_KEY")
    api_url = "https://www.alphavantage.co/query"

    params = {
        "function": "FX_DAILY",
        "from_symbol": from_currency,
        "to_symbol": to_currency,
        "ouputsize": "compact",  # or full
        "datatype": "json",  # or csv
        "apikey": api_key,
    }

    return query_api(api_url, params)


def process_alpha_vantage_fx_response(data):
    for key, value in data["Meta Data"].items():
        print(f"{key}={value}")
    for key, value in data["Time Series FX (Daily)"].items():
        print(f"{key}={value}")


def alpha_vantage_symbol_search(keywords):
    api_key = get_api_key("ALPHA_VANTAGE_KEY")
    api_url = "https://www.alphavantage.co/query"

    params = {"function": "SYMBOL_SEARCH", "keywords": keywords, "apikey": api_key}

    return query_api(api_url, params)


def get_alpha_vantage_tw_stock_data(symbol):
    api_key = get_api_key("ALPHA_VANTAGE_KEY")
    api_url = "https://www.alphavantage.co/query"

    params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": api_key}

    return query_api(api_url, params)
