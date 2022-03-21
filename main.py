from flask import redirect, render_template, jsonify, request, url_for
from flask_login import login_user, logout_user
from app import app, login_manager, db
from app.models import User

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # if nome and email and senha:
        user = User(nome, email, senha)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(senha):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


app.run(debug=True)