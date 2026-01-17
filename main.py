from flask import Flask, render_template, request, redirect, url_for, flash,session
from werkzeug.utils import secure_filename

from models import Proveedor, Producto, Pedido, DetallePedido, Cliente
import db
import os
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
    lista_productos = db.session.query(Producto).all()
    print(lista_productos)
    return render_template("productos.html",productos=lista_productos)

@app.route('/registro-producto')
def registroProducto():
    lista_proveedores = db.session.query(Proveedor).all()
    return render_template("registro-producto.html",proveedores=lista_proveedores)

@app.route('/registro-proveedor')
def registroProveedor():
    return render_template("registro-proveedor.html")


@app.route('/detalle-producto/<int:id>')
def detalleProducto(id):
    producto=db.session.query(Producto).filter_by(id=id).first()
    proveedor_actual = db.session.query(Proveedor).filter_by(id=producto.id_proveedor).first()
    return render_template('registro-producto.html',producto=producto,proveedor_actual=proveedor_actual)


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
    try:
        archivo = request.files.get('imagen')
        nombre_imagen = "default.png"

        if archivo and archivo.filename != '':
            try:
                filename = secure_filename(archivo.filename)
                folder_path = os.path.join(app.root_path, 'static', 'img', 'productos')

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                ruta_completa = os.path.join(folder_path, filename)
                archivo.save(ruta_completa)
                nombre_imagen = filename
            except Exception as e_img:
                print(f"Error al guardar la imagen: {e_img}")
                nombre_imagen = "default.png"

        nuevo_producto = Producto(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            precio_compra=float(request.form.get('precio_compra') or 0),
            precio_venta=float(request.form.get('precio_venta') or 0),
            stock_actual=int(request.form.get('stock_actual') or 0),
            stock_minimo=int(request.form.get('stock_minimo') or 0),
            color=request.form.get('color'),
            referencia=request.form.get('referencia'),
            ubicacion=request.form.get('ubicacion'),
            imagen=nombre_imagen,
            id_proveedor=request.form.get('proveedor_id')
        )

        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('productos'))

    except Exception as e:
        db.session.rollback()
        print(f"Error general en createProducto: {e}")
        return "Hubo un error al guardar el producto", 500




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