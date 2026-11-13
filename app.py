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
        symbol = request.form["symbol"]
        chart_type = request.form["chart_type"]
        time_series = request.form["time_series"]
        start_date_string = request.form["start_date"]
        end_date_string = request.form["end_date"]

        try:
            start_date = datetime.strptime(
                start_date_string,
                "%Y-%m-%d"
            ).date()

            end_date = datetime.strptime(
                end_date_string,
                "%Y-%m-%d"
            ).date()

            if end_date < start_date:
                error_message = (
                    "The end date cannot be before "
                    "the start date."
                )

            else:
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

        except ValueError:
            error_message = "Please enter valid dates."

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