from flask import Flask
from flask import render_template
from flask import request

from database import DB

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    number = None
    if request.method == 'POST':
        try:
            a = float(request.form["numA"])
            b = float(request.form["numB"])
            if b == 0:
                raise ZeroDivisionError
        except ValueError:
            return render_template('index.html', error="Must imput numbers")
        except ZeroDivisionError:
            return render_template('index.html', error="Number B mustn't be zero")
        with DB() as db:
            db.execute("INSERT INTO numbers (numA, numB, data) VALUES (%s, %s, %s)",
                        (a, b, request.form["data"]))
            db.execute("SELECT id, numA, numB FROM numbers ORDER BY id DESC")
            id, numA, numB = db.fetchone()
            number = numA/numB + id
    return render_template('index.html', number=number)
