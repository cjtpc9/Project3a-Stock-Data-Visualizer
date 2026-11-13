import requests
import pygal
from datetime import datetime


def load_api_key():
    with open("api_key.txt", "r") as file:
        return file.read().strip()


def get_stock_data(symbol, time_series, api_key):
    url = "https://www.alphavantage.co/query"

    functions = {
        "Intraday": (
            "TIME_SERIES_INTRADAY",
            "Time Series (60min)"
        ),
        "Daily": (
            "TIME_SERIES_DAILY",
            "Time Series (Daily)"
        ),
        "Weekly": (
            "TIME_SERIES_WEEKLY",
            "Weekly Time Series"
        ),
        "Monthly": (
            "TIME_SERIES_MONTHLY",
            "Monthly Time Series"
        )
    }

    function_name, data_key = functions[time_series]

    params = {
        "function": function_name,
        "symbol": symbol,
        "apikey": api_key
    }

    if time_series == "Intraday":
        params["interval"] = "60min"

    if time_series == "Daily":
        params["outputsize"] = "compact"

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "Error Message" in data:
            return None, "Invalid stock symbol or API request."

        if "Note" in data:
            return None, (
                "API request limit reached. "
                "Please try again later."
            )

        if "Information" in data:
            if time_series == "Intraday":
                return None, (
                    "Intraday stock data requires "
                    "Alpha Vantage premium access. "
                    "Please select Daily, Weekly, or Monthly."
                )

            return None, (
                "Alpha Vantage could not complete "
                "the request. Please try again later."
            )

        if data_key not in data:
            return None, "Stock data could not be found."

        return data[data_key], None

    except requests.RequestException:
        return None, "Could not connect to Alpha Vantage."

    except ValueError:
        return None, (
            "Invalid response received from Alpha Vantage."
        )


def filter_stock_data(
    stock_data,
    start_date,
    end_date
):
    filtered_data = []

    for timestamp, values in stock_data.items():
        try:
            data_date = datetime.strptime(
                timestamp[:10],
                "%Y-%m-%d"
            ).date()

            if start_date <= data_date <= end_date:
                filtered_data.append(
                    {
                        "timestamp": timestamp,
                        "date": data_date,
                        "open": float(
                            values["1. open"]
                        ),
                        "high": float(
                            values["2. high"]
                        ),
                        "low": float(
                            values["3. low"]
                        ),
                        "close": float(
                            values["4. close"]
                        )
                    }
                )

        except (ValueError, KeyError):
            continue

    filtered_data.sort(
        key=lambda item: item["timestamp"]
    )

    return filtered_data


def create_chart(
    symbol,
    chart_type,
    time_series,
    stock_data,
    start_date,
    end_date
):
    chart_settings = {
        "x_label_rotation": 45,
        "show_minor_x_labels": True,
        "truncate_label": -1,
        "margin_bottom": 100
    }

    if chart_type == "Bar":
        chart = pygal.Bar(**chart_settings)
    else:
        chart = pygal.Line(**chart_settings)

    chart.title = (
        f"Stock Data for {symbol}: "
        f"{start_date.strftime('%Y-%m-%d')} "
        f"to {end_date.strftime('%Y-%m-%d')}"
    )

    chart.x_title = "Date"
    chart.y_title = "Price ($)"

    labels = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []

    for item in stock_data:
        if time_series == "Intraday":
            labels.append(
                item["timestamp"]
            )
        else:
            labels.append(
                item["date"].strftime(
                    "%Y-%m-%d"
                )
            )

        open_prices.append(
            item["open"]
        )

        high_prices.append(
            item["high"]
        )

        low_prices.append(
            item["low"]
        )

        close_prices.append(
            item["close"]
        )

    chart.x_labels = labels

    chart.add(
        "Open",
        open_prices
    )

    chart.add(
        "High",
        high_prices
    )

    chart.add(
        "Low",
        low_prices
    )

    chart.add(
        "Close",
        close_prices
    )

    return chart.render_data_uri()