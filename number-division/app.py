from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from database import DB

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    number = None
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json()
            try:
                a = float(json["numA"])
                b = float(json["numB"])
                print(a,b)
                if b == 0:
                    raise ZeroDivisionError
            except ValueError:
                return "You must enter numbers", 400
            except ZeroDivisionError:
                return "Number B mustn't be zero", 400
            with DB() as db:
                db.execute("INSERT INTO numbers (numA, numB, data) VALUES (%s, %s, %s)",
                            (a, b, json["data"]))
                db.execute("SELECT id, numA, numB FROM numbers ORDER BY id DESC")
                id, numA, numB = db.fetchone()
                number = numA/numB
            return jsonify({"result": float(number), "row":id}), 201
        
            
        return "nice", 201
    elif request.method == 'GET':
        return render_template('index.html', number=number), 200
