from idlelib.iomenu import errors

from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
import csv
from wtforms.validators import DataRequired, URL
from wtforms import StringField, SelectField, TimeField, SubmitField


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Location (Google Maps URL)", validators=[DataRequired(), URL()])
    opening_time = TimeField("Opening Time", validators=[DataRequired()])
    closing_time = TimeField("Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=[("1", "☕"), ("2", "☕☕"), ("3", "☕☕☕"), ("4", "☕☕☕☕️"), ("5", "☕☕☕☕️☕️")], validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Rating", choices=[("1", "💪"), ("2", "💪💪"), ("3", "💪💪💪"), ("4", "💪💪💪💪"), ("5", "💪💪💪💪💪")], validators=[DataRequired()])
    power_rating = SelectField("Power Rating", choices=[("1", "🔌"), ("2", "🔌🔌"), ("3", "🔌🔌🔌"), ("4", "🔌🔌🔌🔌"), ("5", "🔌🔌🔌🔌🔌")], validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = {
            "Cafe Name": form.cafe.data.replace(" ", ""),
            "Location": form.location.data,
            "Open": form.opening_time.data.strftime("%I:%M %p"),
            "Close": form.closing_time.data.strftime("%I:%M %p"),
            "Coffee": "☕" * int(form.coffee_rating.data),
            "Wifi": "💪" * int(form.wifi_rating.data),
            "Power": "🔌" * int(form.power_rating.data),
        }

        # Save to CSV
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=new_cafe.keys())
            # Only write the header if the file is empty
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(new_cafe)
        flash('Cafe added successfully!', 'success')
        return redirect(url_for('cafes'))
    else:
        print("Validation errors:", form.errors)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    csv_path = "cafe-data.csv"
    try:
        cafes_df = pd.read_csv(csv_path)
    except pd.errors.ParserError as e:
        print("Error reading CSV:", e)
        return "Error processing the CSV file. Please check the data format.", 500
    cafe_list = cafes_df.to_dict(orient="records")
    return render_template("cafes.html", cafes=cafe_list)


if __name__ == '__main__':
    app.run(debug=True)
