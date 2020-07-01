from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from database import DB

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@app.route('/', methods=['POST', 'GET'])
@limiter.limit("10/minute", override_defaults=False)
def index():
    number = None
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json()
            try:
                a = float(json["numA"])
                b = float(json["numB"])
                print(a, b)
                if b == 0:
                    raise ZeroDivisionError
            except ValueError:
                return "You must enter numbers", 400
            except ZeroDivisionError:
                return "Number B mustn't be zero", 400
            with DB() as db:
                db.execute("INSERT INTO numbers (numA, numB, data) VALUES (%s, %s, %s)",
                           (a, b, json["data"]))
                db.execute(
                    "SELECT id, numA, numB FROM numbers ORDER BY id DESC")
                id, numA, numB = db.fetchone()
                number = numA/numB
            return jsonify({"result": float(number), "row": id}), 201
    elif request.method == 'GET':
        return render_template('index.html', number=number), 200
