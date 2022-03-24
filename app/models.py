from decimal import Decimal
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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

    def __init__(self, nome, email, senha, perfil=2):
        self.nome = nome,
        self.email = email,
        self.senha = generate_password_hash(senha),
        self.perfil = perfil
        
    def verify_password(self, senha):
        return check_password_hash(self.senha, senha)

class Aviso(db.Model):
    __tablename__= 'avisos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    info = db.Column(db.String(50), nullable=False)

    def __init__(self, info):
        self.info = info

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

# class Produtos(db.Model):
#     __tablename__ ='produtos'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     nome = db.Column(db.String(120), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     describe = db.Column(db.String(255), nullable=False)
