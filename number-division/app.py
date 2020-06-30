from flask import Flask
from flask import render_template
from flask import request

from database import DB

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    number = None
    if request.method == 'POST':
        with DB() as db:
            db.execute("INSERT INTO numbers (numA, numB, data) VALUES (%s, %s, %s)",
                        (request.form["numA"], request.form["numB"], request.form["data"]))
            db.execute("SELECT id, numA, numB FROM numbers ORDER BY id DESC")
            id, numA, numB = db.fetchone()
            number = numA/numB + id
    return render_template('index.html', number=number)
