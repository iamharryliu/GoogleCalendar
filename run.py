import os
from flask import Flask, render_template, jsonify, redirect, url_for
from google_calendar import calendar_api
from forms import CredentialForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"


@app.route("/")
def index():
    if os.path.isfile("./credentials.json"):
        yourcalendar = calendar_api()
        pie_chart = yourcalendar.getPieChartDataForNext7Days()
        column_chart = yourcalendar.getColumnChartDataForNextXWeeks(4)
        return render_template(
            "index.html", pie_chart=pie_chart, column_chart=column_chart
        )
    else:
        return redirect(url_for("credential_form"))


@app.route("/credential_form", methods=["GET", "POST"])
def credential_form():
    form = CredentialForm()
    if form.validate_on_submit():
        form.credential.data.save("./credentials.json")
        return redirect(url_for("index"))
    return render_template("credential_form.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
