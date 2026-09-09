from flask import Flask, render_template
from datetime import date, timedelta

app = Flask(__name__)


@app.route("/")
def home():

    today = date.today()
    yesterday = today - timedelta(days=1)

    return render_template(
        "index.html",
        today=today,
        yesterday=yesterday
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)