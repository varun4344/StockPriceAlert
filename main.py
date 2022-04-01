from flask import Flask, render_template, request
import requests
from twilio.rest import Client



app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        STOCK_NAME = request.form.get("stockname").upper()
        COMPANY_NAME = request.form.get("companyname").upper()
        PHONE_NUMBER = request.form.get("phone")


        STOCK_ENDPOINT = "https://www.alphavantage.co/query"
        NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

        STOCK_ACCESS_KEY = "175T5NNFGWPKBIYQ"
        NEWS_ACCESS_KEY = "709a529d4b194a3897c058c15cfae43f"

        TWILIO_SID = "ACa1f56a32c07a5fee60b963695dec14f2"
        TWILIO_TOKEN = "5e4db6f24b6ea7953e652458633cfcb1"

        parameters1 = {
            "function": "TIME_SERIES_DAILY",
            "symbol": STOCK_NAME,
            "apikey": STOCK_ACCESS_KEY
        }

        response = requests.get(STOCK_ENDPOINT, params=parameters1)
        data = response.json()["Time Series (Daily)"]

        data_list = [value for (key, value) in data.items()]
        yesterday_data = data_list[0]
        yesterday_closing_price = float(yesterday_data["4. close"])

        day_before_data = data_list[1]
        day_before_cp = float(day_before_data["4. close"])

        difference = yesterday_closing_price - day_before_cp
        up_down = None
        if difference > 0:
            up_down = "⬆️"
        else:
            up_down = "⬇️"

        percentage_difference = round(100 * abs(difference) / yesterday_closing_price)

        if (percentage_difference > 5):
            parameters2 = {
                "q": COMPANY_NAME,
                "apikey": NEWS_ACCESS_KEY
            }

            response = requests.get(NEWS_ENDPOINT, params=parameters2)
            data = response.json()["articles"]

            three_articles = data[:3]
            articles_list = [
                f"{STOCK_NAME}{up_down}{percentage_difference}% \nHeadline : {article['title']}. \nBrief:{article['description']}"
                for article in three_articles]

            client = Client(TWILIO_SID, TWILIO_TOKEN)
            for article in articles_list:
                message = client.messages.create(
                    body=article,
                    from_="+17066402775",
                    to= PHONE_NUMBER
                )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


print(PHONE_NUMBER)