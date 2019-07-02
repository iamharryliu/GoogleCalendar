from flask import Flask, render_template, jsonify

app = Flask(__name__)

from google_calendar import calendarAPI


@app.route("/")
def index():
    yourcalendar = calendarAPI()
    pie_chart = yourcalendar.getPieChartDataForNext7Days()
    column_chart = yourcalendar.getColumnChartDataForNextXWeeks(4)
    return render_template("index.html", pie_chart=pie_chart, column_chart=column_chart)


if __name__ == "__main__":
    app.run(debug=True)
