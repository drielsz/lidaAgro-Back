from cgi import test
from functools import wraps
import json
from flask import redirect, render_template, request, url_for, flash, current_app, session, jsonify, make_response
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.models import User, Aviso, Produtos, Atendimento
import os
from dotenv import load_dotenv
import secrets
import stripe
import pdfkit

load_dotenv()

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}

publishable_key = stripe_keys["publishable_key"]

stripe.api_key = stripe_keys["secret_key"]

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            flash("Você precisa fazer login primeiro.", "danger")
            return redirect(request.referrer)

    return wrap

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    subtotal = 0
    grandtotal = 0
    for key, produto in session['Shoppingcart'].items():
        desconto = (produto['desconto']/100) * float(produto['price'])
        subtotal += float(produto['price']) * int(produto['quantidade'])
        subtotal -= desconto
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = ("%.2f" % (1.06 * float(subtotal)))
    return render_template('/checkout/index.html', tax=tax, grandtotal=grandtotal)

@app.route('/boleto', methods=['GET', 'POST'])
def boleto():
    return render_template('boleto.html')

@app.route('/testprodutos', methods=['GET', 'POST'])
def testprodutos():
    produtos = Produtos.query.all()
    return render_template('teste/produtos.html', produtos = produtos)

@app.route('/config')
def config():
    return jsonify({'publishableKey' : stripe_keys['publishable_key']})

# Intenção de compra do usuario ( boleto, cartão.. )
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        payment_method_type = data['paymentMethodType']
        currency = data['currency']

        payment_intent = stripe.PaymentIntent.create(
            amount = 1999,
            currency= currency,
            payment_method_types=[payment_method_type]
        )
        return jsonify({'clientSecret' : payment_intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify({'error':{'message' : e.user_message}}), 400
    except Exception as e:
        return jsonify({'error' : {'message' :  e.user_message}}), 500


@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
    return jsonify({'status': 'success'})

@app.route('/payment', methods=['POST'])
def payment():
    data = request.form
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=data['stripeEmail'],
        source=data['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Lida Agropecuária',
        amount=amount,
        currency='brl',
    )
    return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
    produtos = Produtos.query.all()
    subtotal = 0
    grandtotal = 0
    for key, produto in session['Shoppingcart'].items():
        desconto = (produto['desconto']/100) * float(produto['price'])
        subtotal += float(produto['price']) * int(produto['quantidade'])
        subtotal -= desconto
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = ("%.2f" % (1.06 * float(subtotal)))
    desconto = (produto['desconto']/100) * float(produto['price'])
    subtotal += float(produto['price']) * int(produto['quantidade'])
    subtotal -= desconto
    tax = ("%.2f" % (.06 * float(subtotal)))
    grandtotal = ("%.2f" % (1.06 * float(subtotal)))
    amount = grandtotal.replace('.', '')
    return render_template('thank.html', tax=tax, grandtotal=amount, produtos=produtos)
    
@app.route('/')
def home():
    produtos = Produtos.query.limit(4).all()
    return render_template('home.html', produtos=produtos)

# Filtros


@app.route('/category_filter=?sementes')
def filter_by_sementes():
    produtos = Produtos.query.filter_by(categoria="sementes").all()
    return render_template('produtos/result.html', produtos=produtos)

# Filtros


@app.route('/category_filter=?substrato')
def filter_by_substrato():
    produtos = Produtos.query.filter_by(categoria="substrato").all()

    return render_template('produtos/result.html', produtos=produtos)

# Filtros


@app.route('/category_filter=?biologico')
def filter_by_biologico():
    produtos = Produtos.query.filter_by(categoria="biologico").all()

    return render_template('produtos/result.html', produtos=produtos)

# Filtros


@app.route('/category_filter=?adubo_foliar')
def filter_by_aduboF():
    produtos = Produtos.query.filter_by(categoria="Adubo Foliar").all()

    return render_template('produtos/result.html', produtos=produtos)

# Filtros


@app.route('/category_filter=?ofertas')
def filter_by_ofertas():
    produtos = Produtos.query.filter(Produtos.desconto > 0)

    return render_template('produtos/result.html', produtos=produtos)


@app.route('/lida-agro')
def lida_agro():
    produtos = Produtos.query.limit(3).all()
    return render_template('error404.html')
    # return render_template('quem_somos.html', produtos=produtos)


@app.route('/result')
def result():
    searchword = request.args.get('q')
    # Limit = Limite de quantos resultados vão voltar
    # Fields = Pesquise por ('nome', 'desc')
    produtos = Produtos.query.msearch(searchword, fields=['nome', 'desc'])
    allprodutos = Produtos.query.all()
    return render_template('produtos/result.html', produtos=produtos, allprodutos=allprodutos)


@app.route('/produtos=?user=?cliente', methods=['GET', 'POST'])
def produtos_cliente():
    produtos = Produtos.query.filter(Produtos.estoque > 0)
    return render_template('produtos.html', produtos=produtos)


@app.route('/produtos?=cliente?<int:id>')
def single_page(id):
    produto = Produtos.query.get_or_404(id)
    return render_template('single_page.html', produto=produto)


# Add Carrinho
def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/get_pdf/<invoice>', methods=['POST'])
def get_pdf(invoice):
    produtos = Produtos.query.all()
    if current_user.is_authenticated:
        grandtotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = customer_id
            orders = customer_id
            for key, produto in session['Shoppingcart'].items():
                desconto = (produto['desconto']/100) * float(produto['price'])
                subTotal += float(produto['price']) * int(produto['quantidade'])
                subTotal -= desconto
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandtotal = ("%.2f" % (1.06 * float(subTotal)))
            rendered = render_template('pdf.html', invoice=invoice, tax=tax, grandtotal=grandtotal, customer=customer, orders=orders, produtos=produtos)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='atteched; filename='+invoice+'.pdf'
            return response

    return request(url_for('getCart'))

@app.route('/addcarrinho', methods=['POST'])
def AddCarrinho():
    try:
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')
        produto = Produtos.query.filter_by(id=produto_id).first()
        if produto and quantidade and produto_id and request.method == 'POST':
            # Passando as informações para o carrinho
            DictItems = {produto_id: {'nome': produto.nome, 'price': produto.price, 'desconto': produto.desconto,
            'quantidade': quantidade, 'image': produto.image, 'estoque': produto.estoque}}
            # End
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                flash("Item colocado no carrinho com sucesso", 'success')
                if produto_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(produto_id):
                            session.modified = True
                            item['quantidade'] += 1
                            flash("Item colocado no carrinho com sucesso", 'success')

                else:
                    session['Shoppingcart'] = MagerDicts(
                        session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print('Erro na hora de adicionar produto ao carrinho erro', e)
    finally:
        return redirect(request.referrer)


@app.route('/carrinho?user=?')
def getCart():
    try:
        if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
            flash('Nenhum item no carrinho', 'danger')
            return redirect(url_for('produtos_cliente'))
    except Exception as e:
        print(e)
        pass

    subtotal = 0
    grandtotal = 0
    for key, produto in session['Shoppingcart'].items():
        desconto = (produto['desconto']/100) * float(produto['price'])
        subtotal += float(produto['price']) * int(produto['quantidade'])
        subtotal -= desconto
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = ("%.2f" % (1.06 * float(subtotal)))

    return render_template('produtos/carts.html', tax=tax, grandtotal=grandtotal)


@app.route('/atualizarcarrinho/<int:code>', methods=['POST'])
def atualizar_carrinho(code):
    # Key = Code
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))

    if request.method == 'POST':
        quantidade = request.form.get('quantidade')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantidade'] = quantidade
                    flash('Item atualizado com sucesso. Boas compras', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            flash(e, 'danger')
            return redirect(url_for('getCart'))


@app.route('/deleteitem/<int:id>')
def delete_item(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        flash("Sem nenhum item no carrinho.", 'info')
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                flash("Item retirado pelo cliente do carrinho.", 'info')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/limparcarrrinho')
def limpar_carrinho():
    try:
        # Session pop para remover SOMENTE SHOPPING CART, NÃO USE SESSION.CLEAR() PQ SE NAO VAI DELETAR TODAS AS SESSOES,
        # O QUE QUEREMOS AQUI É SOMENTE DELETAR A SESSÃO ATUAL DO SHOPPING CART.
        session.pop('Shoppingcart', None)
        flash("Item retirado do carrinho", 'warning')
        return redirect(url_for('produtos_cliente'))
    except Exception as e:
        print(e)
# End Add Carrinho


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']

            senha = request.form['senha']

            # if nome and email and senha:
            user = User(nome, email, senha)
            db.session.add(user)
            db.session.commit()
            flash("Conta cadastrada com sucesso", 'success')
            return redirect(url_for('login'))
    except Exception as e:
        pass
        print(e)
        if "Duplicate entry" in str(e.__cause__):
            flash("O endereço de e-mail já existe", 'danger')
        else:
            print(e)

    return render_template('register.html')


@app.route('/atendimento', methods=['GET', 'POST'])
def atendimento():
    if request.method == 'POST':
        assunto = request.form['assunto']
        email = request.form['email']
        nome = request.form['nome']
        telefone = request.form['telefone']
        estado = request.form['estado']
        cidade = request.form['cidade']
        descricao = request.form['descricao']

        atendimento = Atendimento(
            assunto=assunto,
            nome=nome,
            email=email,
            cidade=cidade,
            estado=estado,
            telefone=telefone,
            descricao=descricao)
        db.session.add(atendimento)
        db.session.commit()

        return redirect(request.referrer)

    return render_template('atendimento.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(senha):
            flash("Por favor, verifique seus dados de login e tente novamente.", 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash(
            "As informações estavam corretas e o login foi sucessivo. Parabéns", 'success')
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    return render_template('forgotpassword.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Saiu da conta', 'danger')
    return redirect(request.referrer)


@app.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('admin/dashboard.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
   ip = request.remote_addr
   print(ip)
   if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(senha):
            return redirect(url_for('admin_login'))

        login_user(user)

        return redirect(url_for('dashboard'))
   if ip != '127.0.0.1':
       return jsonify(message="ENTRADA NAO ESTA DISPONIVEL")
   else:
       return render_template('admin/admin_login.html')


@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    ip = request.remote_addr
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # if nome and email and senha:
        user = User(nome, email, senha, 0, image='null')
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin_login'))
    if ip != '127.0.01':
        return jsonify(message="ENTRADA NAO ESTA DISPONIVEL")
    else:
        return render_template('admin/registrar/register.html')


@app.route('/admin/register/funcionario', methods=['GET', 'POST'])
def register_funcionario():
    funcionarios = User.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user = User(nome, email, senha, 1)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('register_funcionario'))

    return render_template('admin/registrar/funcionario.html', funcionarios=funcionarios)


@app.route('/admin/register/aviso', methods=['GET', 'POST'])
def register_aviso():
    funcionarios = User.query.all()
    avisos = Aviso.query.all()
    if request.method == 'POST':
        info = request.form['info']

        informacao = Aviso(info)
        db.session.add(informacao)
        db.session.commit()

        return redirect(url_for('register_aviso'))

    return render_template('admin/registrar/aviso.html', avisos=avisos, funcionarios=funcionarios)


def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path,
                             'static/assets/posts', photo_name)
    photo.save(file_path)
    return photo_name

# Adicionar produto


@app.route("/admin/addproduto", methods=['GET', 'POST'])
def addproduto():
    if request.method == 'POST':
        texto = request.form['nome']
        nome = texto.upper()
        price = request.form['price']
        desconto = request.form['desconto']
        estoque = request.form['estoque']
        desc = request.form['desc']
        photo = save_images(request.files['photo'])
        categoria = request.form['categoria']

        post = Produtos(nome=nome,
                        price=price, desconto=desconto,
                        estoque=estoque, desc=desc,
                        image=photo, categoria=categoria)

        db.session.add(post)
        db.session.commit()
    return render_template('admin/add_product.html')

# Olhar os produtos


@app.route("/admin/produtos", methods=['GET', 'POST'])
def produtos():
    produtos = Produtos.query.all()
    return render_template('admin/show_product.html', produtos=produtos)

# Delete


@app.route("/delete_produto/<int:id>/", methods=['POST'])
def delete_produto(id):
    produto = Produtos.query.get(id)
    if request.method == 'POST':
        db.session.delete(produto)
        db.session.commit()

        return redirect(url_for('dashboard'))
    return redirect(url_for('addproduct'))

# Atualizar Produto


@app.route("/admin/atualizar_produto/<int:id>/", methods=['GET', 'POST'])
def atualizar_produto(id):
    produto = Produtos.query.get(id)
    if request.method == 'POST':
        texto = request.form['nome']
        nome = texto.upper()
        price = request.form['price']
        desconto = request.form['desconto']
        estoque = request.form['estoque']
        desc = request.form['desc']
        photo = save_images(request.files['photo'])

        produto.nome = nome
        produto.price = price
        produto.desconto = desconto
        produto.estoque = estoque
        produto.desc = desc
        produto.image = photo

        db.session.commit()
    return render_template('admin/atualizar_produto.html', produto=produto)


@app.route("/quem-somos", methods=['GET'])
def quem_somos():
    return render_template("quem_somos.html")


@app.route("/admin/perfil/<int:id>/", methods=['GET', 'POST'])
def admin_perfil(id):
    user = User.query.get(id)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        biografia = request.form['biografia']
        photo = save_images(request.files['photo'])

        user.nome = nome
        user.email = email
        user.biografia = biografia
        user.image = photo

        db.session.commit()
    return render_template('admin/perfil.html')


if __name__ == '__main__':
    app.run(port=4242, debug=True)
