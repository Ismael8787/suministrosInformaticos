from flask import Flask, render_template, request, redirect, url_for, flash,session
from models import Proveedor, Producto, Pedido, DetallePedido, Cliente
import db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'circuit-box-dev-key'

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/productos')
def productos():
    return render_template("productos.html")


@app.route('/registro-cliente', methods=['POST'])
def crearCliente():
    cliente = Cliente(
        nombre=request.form.get('nombre'),
        apellido=request.form.get('apellido'),
        email=request.form.get('email'),
        telefono=request.form.get('telefono'),
        direccion=request.form.get('direccion'),
        username=request.form.get('usuario'),
        password=generate_password_hash(request.form.get('password')),
    )
    try:
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        print("ERROR SQLAlchemy:", e)
        return redirect(url_for('registro'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    cliente = db.session.query(Cliente).filter_by(email=email).first()

    if cliente and check_password_hash(cliente.password, password) :
        session['userId'] = cliente.id
        session['username'] = cliente.username
        return redirect(url_for('productos'))
    else:
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('home'))



if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)