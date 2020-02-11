from flask import Flask, Response, render_template, request
from wtforms import TextField, Form, SubmitField
from wtforms.validators import DataRequired 
from flask import jsonify
import mysql.connector
from mysql.connector import Error
from flask_fontawesome import FontAwesome


app = Flask(__name__)
fa = FontAwesome(app)


def get_details(res):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", database="shopdb", password="")
        curr = conn.cursor(buffered=True)

        values = []
        for item in res:
            val = item
            curr.execute('select * from cities where city = %s', (val,))
            result = curr.fetchone()
            values.append(result)
        
        return values

    except Error as e:
        print(e)

    finally:
        curr.close()
        conn.close()


def get_cities():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", database="shopdb", password="")
        cursor = conn.cursor()
        cursor.execute('select city from cities')

        results = cursor.fetchall()
        
        return results

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


results = get_cities()
locations_list = list(map(lambda tuple_item: tuple_item[0], results))


class GetForm(Form):
    search_box = TextField('', id='autocomplete', validators=[DataRequired()])
    search_button = SubmitField('', id='search_button')


@app.route('/place', methods=['GET'])
def place():
    return jsonify(json=locations_list)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        res = request.get_json().get('locations')
        values = get_details(res)

        return render_template("index.html", res=values)

    return render_template("index.html")


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    form = GetForm(request.form)
    if request.method == 'POST':
        res = form.search_box.data

        conn = mysql.connector.connect(host="localhost", user="root", database="shopdb", password="")
        curr = conn.cursor(buffered=True)
        curr.execute('select * from cities where city = %s', (res,))
        result = curr.fetchone()

        return render_template("locations.html",form=form, res=result)


if __name__ == '__main__':
    app.run(debug=True)
