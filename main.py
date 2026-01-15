from flask import Flask, render_template, request, redirect, url_for, flash,session
from werkzeug.utils import secure_filename

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

@app.route('/registro-producto')
def registroProducto():
    lista_proveedores = db.session.query(Proveedor).all()
    return render_template("registro-producto.html",proveedores=lista_proveedores)

@app.route('/registro-proveedor')
def registroProveedor():
    return render_template("registro-proveedor.html")


@app.route('/create-cliente', methods=['POST'])
def createCliente():
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


@app.route('/create-proveedor', methods=['POST'])
def createProveedor():
    descuento=0.0;
    iva=0.0;
    if request.form.get('descuento') :
        descuento=float(request.form.get('descuento'))

    if request.form.get('iva') :
        iva=float(request.form.get('iva'))


    proveedor = Proveedor(
        nombre=request.form.get('nombre'),
        cif=request.form.get('cif'),
        email=request.form.get('email'),
        telefono=request.form.get('telefono'),
        direccion=request.form.get('direccion'),
        iva=iva,
        descuento=descuento,
    )
    try:
        db.session.add(proveedor)
        db.session.commit()
        return redirect(url_for('productos'))
    except Exception as e:
        db.session.rollback()
        print("ERROR SQLAlchemy:", e)
        return redirect(url_for('registroProveedor'))




@app.route('/create-producto', methods=['POST'])
def createProducto():
    nombre = request.form.get('nombre')
    archivo = request.files.get('imagen')
    nombre_imagen = "default.png"

    if archivo and archivo.filename != '':
        filename = secure_filename(archivo.filename)
        nombre_imagen = filename

    proveedor = Proveedor(
        nombre=request.form.get('nombre'),
        descripcion=request.form.get('descripcion'),
        precio_compra=request.form.get('email'),
        precio_venta=request.form.get('telefono'),
        stock_actual=request.form.get('direccion'),
        stock_minimo=request.form.get('minimo'),
        color=request.form.get('color'),
        referencia=request.form.get('referencia'),
        ubicacion=request.form.get('ubicacion'),
        imagen=nombre_imagen,
        id_proveedor=request.form.get('proveedor_id'),
    )

    try:
        db.session.add(proveedor)
        db.session.commit()
        return redirect(url_for('productos'))
    except Exception as e:
        db.session.rollback()
        print("ERROR SQLAlchemy:", e)
        return redirect(url_for('registroProveedor'))



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