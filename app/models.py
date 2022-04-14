from decimal import Decimal

from sqlalchemy import ForeignKey
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)
    perfil = db.Column(db.Integer, default=2)
    image = db.Column(db.Text(150), default='https://images.unsplash.com/photo-1548247416-ec66f4900b2e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=720&q=80')
    biografia = db.Column(db.String(86), default='Amor por animais e fazenda.')

    def __init__(self, nome, email, senha, perfil=2, image='', biografia='Amor por animais e fazenda.'):
        self.nome = nome,
        self.email = email,
        self.senha = generate_password_hash(senha),
        self.perfil = perfil
        self.image = image
        self.biografia = biografia
        
    def verify_password(self, senha):
        return check_password_hash(self.senha, senha)

class Aviso(db.Model):
    __tablename__= 'avisos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    info = db.Column(db.String(50), nullable=False)

    def __init__(self, info):
        self.info = info

class Produtos(db.Model):
    __tablename__ ='produtos'
    __seachbale__ = ['nome', 'desc']
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    desconto = db.Column(db.Integer, default=0)
    estoque = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    data = db.Column(db.LargeBinary)
    image = db.Column(db.Text(150), nullable=False)
    categoria = db.Column(db.String(80))
    
    def __init__(self, nome, price, desconto, estoque, desc, image, categoria):
        self.nome = nome,
        self.price = price,
        self.desconto= desconto,
        self.estoque = estoque,
        self.desc = desc,
        self.image = image,
        self.categoria = categoria

class Pedidos(db.Model):
    __tablename__ = 'pedidos' 
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    produto_id = db.Column(db.Integer, ForeignKey('produtos.id'))
    user_id =  db.Column(db.Integer, ForeignKey('users.id'))

class Atendimento(db.Model):
    __tablename__ = 'atendimentos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    assunto = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False)
    nome = db.Column(db.String(86), nullable=False)
    telefone = db.Column(db.String(12), nullable=False)
    cidade = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(84), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)


    def __init__(self, assunto, nome, email, estado, telefone, cidade, descricao):
        self.assunto = assunto,
        self.email = email,
        self.nome = nome,
        self.telefone = telefone,
        self.cidade = cidade,
        self.estado = estado,
        self.descricao = descricao

    
# class Venda(db.Model):
#     __tablename__ = 'venda'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # valor_total = db.Column(db.Decimal(10,2))
#     data = db.Column(db.DateTime())
#     cliente_id = db.Column(db.Integer, primary_key=True)
#     empresa_id = db.Column(db.Integer, primary_key=True)
#     pagamento_id = db.Column(db.Integer, primary_key=True)

# class Empresa(db.Model):
#     __tablename__ = 'empresa'
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(86))

# class Pagamento(db.Model):
#     __tablename__ = 'pagamento'
#     id = db.Column(db.Integer, primary_key=True)

# class Local_Entrega(db.Model):
#     __tablename__ = 'local_entrega'
#     endereco = db.Column(db.String(255))
#     bairro = db.Column(db.String(255))
#     numero_casa = db.Column(db.Integer)
#     cep = db.Column(db.Integer)

# class Venda_Concluida(db.Model):
#     venda_id = db.Column(db.Integer, primary_key=True)
#     produto_id = db.Column(db.Integer, primary_key=True)
#     local_entrega = db.Column(db.String(255))

# class Categoria(db.Model):
#     id = db.Column(db.Integer)
#     nome = db.Column(db.String(120), nullable=False)

