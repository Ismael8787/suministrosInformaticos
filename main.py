from flask import Flask, render_template, request, redirect, url_for
from models import Proveedor, Producto, Pedido, DetallePedido, Cliente
import db
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/registro')
def registro():
    return render_template("registro.html")

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





if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)