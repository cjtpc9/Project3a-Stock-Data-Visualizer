import csv
from datetime import datetime

from flask import Flask, render_template, request

from stock_visualizer import (
    load_api_key,
    get_stock_data,
    filter_stock_data,
    create_chart
)

app = Flask(__name__)


def load_stock_symbols():
    symbols = []

    with open("stocks.csv", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            symbols.append(row["Symbol"])

    return symbols


@app.route("/", methods=["GET", "POST"])
def index():
    symbols = load_stock_symbols()

    chart_data = None
    error_message = None

    if request.method == "POST":
        symbol = request.form.get("symbol", "").strip()
        chart_type = request.form.get("chart_type", "").strip()
        time_series = request.form.get("time_series", "").strip()
        start_date_string = request.form.get(
            "start_date",
            ""
        ).strip()
        end_date_string = request.form.get(
            "end_date",
            ""
        ).strip()

        valid_chart_types = [
            "Bar",
            "Line"
        ]

        valid_time_series = [
            "Intraday",
            "Daily",
            "Weekly",
            "Monthly"
        ]

        if not symbol:
            error_message = (
                "Please select a stock symbol."
            )

        elif symbol not in symbols:
            error_message = (
                "Invalid stock symbol selected."
            )

        elif chart_type not in valid_chart_types:
            error_message = (
                "Please select a valid chart type."
            )

        elif time_series not in valid_time_series:
            error_message = (
                "Please select a valid time series."
            )

        elif not start_date_string:
            error_message = (
                "Please enter a start date."
            )

        elif not end_date_string:
            error_message = (
                "Please enter an end date."
            )

        else:
            try:
                start_date = datetime.strptime(
                    start_date_string,
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                error_message = (
                    "Please enter a valid start date."
                )
                start_date = None

            try:
                end_date = datetime.strptime(
                    end_date_string,
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                if error_message is None:
                    error_message = (
                        "Please enter a valid end date."
                    )
                end_date = None

            if (
                error_message is None
                and end_date < start_date
            ):
                error_message = (
                    "The end date cannot be before "
                    "the start date."
                )

            if error_message is None:
                api_key = load_api_key()

                stock_data, error_message = get_stock_data(
                    symbol,
                    time_series,
                    api_key
                )

                if stock_data is not None:
                    filtered_data = filter_stock_data(
                        stock_data,
                        start_date,
                        end_date
                    )

                    if not filtered_data:
                        error_message = (
                            "No stock data was found "
                            "for the selected date range."
                        )

                    else:
                        chart_data = create_chart(
                            symbol,
                            chart_type,
                            time_series,
                            filtered_data,
                            start_date,
                            end_date
                        )

    return render_template(
        "index.html",
        symbols=symbols,
        chart_data=chart_data,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )