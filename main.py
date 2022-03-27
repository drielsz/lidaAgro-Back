from flask import redirect, render_template, jsonify, request, url_for, flash, current_app
from flask_login import login_user, logout_user
from app import app, login_manager, db
from app.models import User, Aviso, Produtos
from werkzeug.utils import secure_filename
import os
import secrets

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

        return redirect(url_for('login'))

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

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    return render_template('forgotpassword.html')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(senha):
            return redirect(url_for('admin_login'))

        login_user(user)

        return redirect(url_for('dashboard'))

    return render_template('admin_login.html')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':    
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # if nome and email and senha:
        user = User(nome, email, senha, 0)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin/login'))

    return render_template('register.html')

@app.route('/admin/register/funcionario', methods=['GET', 'POST'])
def register_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user = User(nome, email, senha, 1)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('register_funcionario'))

    return render_template('register_funcionario.html')

@app.route('/admin/register/aviso', methods=['GET', 'POST'])
def register_aviso():
    if request.method == 'POST':
        info = request.form['info']

        informacao = Aviso(info)
        db.session.add(informacao)
        db.session.commit()

        return redirect(url_for('register_aviso'))

    return render_template('register_aviso.html')

def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path, 'static/assets/posts', photo_name)
    photo.save(file_path)
    return photo_name

# Adicionar produto
@app.route("/admin/addproduto", methods=['GET', 'POST'])
def addproduto():
    if request.method =='POST':
        nome = request.form['nome']
        price = request.form['price']
        desconto = request.form['desconto']
        estoque = request.form['estoque']
        desc = request.form['desc']
        photo = save_images(request.files['photo'])

        post = Produtos(nome, price, desconto, estoque, desc, image=photo)

        db.session.add(post)
        db.session.commit()
    return render_template('add_product.html')

# Olhar os produtos
@app.route("/admin/produtos", methods=['GET', 'POST'])
def produtos():
    produtos = Produtos.query.all()
    return render_template('show_product.html', produtos=produtos)

# Delete
@app.route("/delete_produto/<int:id>/", methods=['POST'])
def delete_produto(id):
    produto = Produtos.query.get(id)
    if request.method =='POST':
        db.session.delete(produto)
        db.session.commit()

        return redirect(url_for('dashboard'))
    return redirect(url_for('addproduct'))

@app.route("/admin/register/lista", methods=['GET'])
def lista():
    avisos = Aviso.query.all()
    return render_template("olhar_avisos.html", avisos=avisos)

@app.route("/quem-somos", methods=['GET'])
def quem_somos():
    return render_template("quem_somos.html")


app.run(debug=True)