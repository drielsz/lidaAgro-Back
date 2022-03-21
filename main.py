from flask import render_template, jsonify
from app import app

@app.route("/")
def hello():
    return jsonify("Hello Lida")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

app.run(debug=True)