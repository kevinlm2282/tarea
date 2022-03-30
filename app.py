from flask import Flask
from flask import render_template,request,redirect,url_for,flash,session
from flaskext.mysql import MySQL
from datetime import datetime
import templates.generador as reportePDF
# import webbrowser as wb
import os

app= Flask(__name__)

app.secret_key="kevin"


mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='mydb'
mysql.init_app(app)



@app.route('/inicio')
def inicio():
    if 'nombre' in session:
            print(session)
            sql ="SELECT * FROM `empleado`;"
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute(sql)
            empleados=cursor.fetchall()
            # print(empleados)
            conn.commit()
            return render_template('empleado/inicio.html',empleados=empleados)
    else:
            return render_template('empleado/index.html')
    
            

    

@app.route('/destroy/<int:idUsuarion>')
def destroy(idUsuarion):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("DELETE FROM empleado Where idUsuarion=%s",(idUsuarion))
    conn.commit()
    return redirect('/inicio')

@app.route('/edith/<int:idUsuarion>')
def edith(idUsuarion):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM empleado Where idUsuarion=%s", (idUsuarion))
    empleados=cursor.fetchall()
    # print(empleados)
    conn.commit()
    return render_template('empleado/edith.html',empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
   
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _telefono = request.form['txtTelefono']
    _direccion = request.form['txtDireccion']
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    _admin = request.form['txtAdmin']
    id=request.form['txtID']
    sql ="UPDATE empleado SET Nombre=%s, Apellido=%s, Telefono=%s, Direccion=%s, Usuario=%s, Password=%s, Admin=%s  WHERE idUsuarion=%s;"

    datos=(_nombre,_apellido,_telefono,_direccion,_usuario,_password,_admin,id)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/inicio')
    

@app.route('/create')
def create():
   return render_template('empleado/create.html')



@app.route('/store', methods=['POST'])
def storage():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _telefono = request.form['txtTelefono']
    _direccion = request.form['txtDireccion']
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    _admin = request.form.get('check')
    # if(_admin == '0'):
    #     _adminM = '0'
    #     return _adminM
    # else:
    #     _adminM = '1'
    #     return _adminM

    if _nombre=='' or _apellido=='' or _direccion=='' or _usuario=='' or _password=='' or _telefono=='' or _admin=='':
        flash('recuerda llenar los datos de todos los campos')
        
        return redirect(url_for('create'))


    sql ="INSERT INTO `empleado` (`idUsuarion`, `Nombre`, `Apellido`,`Telefono`,`Direccion`, `Usuario`, `Password`,`Admin` ) VALUES (NULL, %s, %s, %s, %s, %s,%s,%s);"
    

    datos=(_nombre,_apellido,_telefono,_direccion,_usuario,_password, _admin)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/inicio')


@app.route('/salir')
def Salir():
    session.clear()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('empleado/index.html')

@app.route('/', methods=['POST','GET'])
def autenticar():
   idEm = ''
   if (request.method == "GET"):
        if 'nombre' in session:
            return render_template('empleado/inicio.html')
        else:
            return render_template('empleado/index.html')
   else: 
        usuario = request.form['user']
        password = request.form['pass']
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT Nombre, idUsuarion, Admin FROM empleado where Usuario='"+ usuario +"' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash("verifique el usuario y la contraseña", "alert-warning")
            return redirect(url_for('index'))
        else: 
            if data != None:
                if data[2] == 1:
                    session['nombre'] = data[0]
                    session['id'] = data[1]
                    session['admin'] = data[2]
                    return redirect(url_for('inicio'))
                else:
                    session['nombre'] = data[0]
                    session['id'] = data[1]
                    session['admin'] = data[2]
                    return redirect(url_for('producto'))
            else:
                    flash("el correo no existe", "alert warning")
                    return redirect(url_for('index'))

   
@app.route('/producto')
def producto():

   sql = "SELECT * FROM `producto`;"
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute(sql)
   producto = cursor.fetchall()
   conn.commit()
   return render_template('empleado/producto.html',producto=producto)

@app.route('/createProduct')
def createProduct():
   return render_template('empleado/createProduct.html')

@app.route('/destroyProduct/<int:idProducto>')
def destroyProduct(idProducto):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("DELETE FROM producto Where idProducto=%s",(idProducto))
    conn.commit()
    return redirect('/producto')


@app.route('/storeProduct', methods=['POST'])
def storeProduct():
    _concentracion = request.form['txtConcentracion']
    _fechaVenc = request.form['txtFecha']
    _formaFarmaceutica = request.form['txtForma']
    _marca = request.form['txtMarca']
    _nombre = request.form['txtNombre']
    _precio = request.form['txtPrecio']
    _precioComp = request.form['txtPrecioCompra']
    _receta = request.form['txtReceta']
    _stock = request.form['txtstock']


    if _concentracion=='' or _fechaVenc=='' or _formaFarmaceutica=='' or _marca=='' or _nombre=='' or _precio=='' or _precioComp=='' or _receta=='' or _stock=='':
        flash('recuerda llenar los datos de todos los campos')
        return redirect(url_for('createProduct'))


    sql ="INSERT INTO `producto` (`idProducto`, `Concentracion`, `Fecha de vencimiento`,`Forma farmaceutica`,`Marca`, `Nombre Producto`, `Precio`,`Precio de compra`,`receta`,`stock` ) VALUES (NULL, %s, %s, %s, %s, %s,%s,%s,%s,%s);"
    

    datos=(_concentracion,_fechaVenc,_formaFarmaceutica,_marca,_nombre,_precio, _precioComp,_receta, _stock)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute(sql,datos)
    print(cursor)
    conn.commit()
    return redirect('/producto')


@app.route('/edithProduct/<int:idProducto>')
def edithProduct(idProducto):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM producto Where idProducto=%s", (idProducto))
    producto=cursor.fetchall()
    # print(empleados)
    conn.commit()
    return render_template('empleado/edithProduct.html',producto=producto)


@app.route('/updateProduct', methods=['POST'])
def updateProduct():

    _concentracion = request.form['txtConcentracion']
    _fechaVenc = request.form['txtFecha']
    _formaFarmaceutica = request.form['txtForma']
    _marca = request.form['txtMarca']
    _nombre = request.form['txtNombre']
    _precio = request.form['txtPrecio']
    _precioComp = request.form['txtPrecioCompra']
    _receta = request.form['txtReceta']
    _stock = request.form['txtstock']
    id=request.form['txtID']
    # _precio1 = float(_precio)
    # _precio2 = float(_precioComp)
    # _st = int(_stock)
    sql ="UPDATE producto SET Concentracion=%s, `Fecha de vencimiento`=%s, `Forma farmaceutica`=%s, `Marca`=%s, `Nombre Producto`=%s, `Precio`=%s, `Precio de compra`=%s, `receta`=%s, `stock`=%s    WHERE idProducto=%s;"
    datos=(_concentracion,_fechaVenc,_formaFarmaceutica,_marca,_nombre,_precio,_precioComp,_receta,_stock,id)
    
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute(sql,datos)
    print(cursor)
    conn.commit()
    return redirect('/producto')

@app.route('/busc')
def busc():
   return render_template('empleado/ventaBusc.html')    

@app.route('/venta',methods=['POST'])
def venta():
   idB = request.form['txtid']
   idC = request.form['txtidCli']
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor1 = conn.cursor()
   cursor.execute("SELECT idProducto, `Nombre Producto`, `Marca`, `Forma farmaceutica`, `Concentracion`    FROM producto where idProducto='"+ idB +"'")
   cursor1.execute("SELECT CI, Nombre, Apellido  FROM cliente where CI='"+idC+"'")
   data = cursor.fetchall()
   cli = cursor1.fetchall()
   conn.commit() 
   print(data)     
   print(cli)
   return render_template('empleado/ventadatos.html',data=data, cli=cli)


@app.route('/ventadatos')
def ventadatos():
   return render_template('empleado/ventadatos.html')

@app.route('/updateSale', methods=['POST','GET'])
def updateSale():
    
    _ID = request.form['txtID']
    _nombreProducto = request.form['txtNombre']
    _Marca = request.form['txtMarca']
    _Forma = request.form['txtforma']
    _Con = request.form['txtCon']
    _CI = request.form['txtCI']
    _Nom = request.form['txtNom']
    _Ap = request.form['txtAp']
    _cantidad = request.form['txtCantidad']
    _cant = int(_cantidad)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT stock, precio FROM producto WHERE idProducto='"+_ID+"'")
    stock = cursor.fetchall()
    conn.commit()
    stockf = ((stock[0])[0])
    precioUnit =((stock[0])[1])
    if stockf < _cant:
        flash('No hay suficientes producto en stock')
        conn.commit()
        now = datetime.now()
        print(now.date())
        print(now.day)
        print(session['id'])
        return redirect(url_for('busc'))
    else:
        now = datetime.now()
        fechaToday = now.date()
        totalPag = _cant * precioUnit
        stockT = stockf - _cant
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()
        cursor4 = conn.cursor()
        sql = "UPDATE producto SET stock=%s WHERE idProducto=%s"
        datos = (stockT,_ID)
        sql2 ="INSERT INTO `venta` (`idVenta`, Fecha, Total, Cliente_CI, Usuarion_idUsuarion) VALUES (NULL, %s, %s, %s, %s);"
        datos2 = (fechaToday, totalPag, _CI, session['id'])
        sql3 = "SELECT idProducto, `Nombre Producto`, Marca FROM producto  WHERE idProducto=%s"
        cursor2.execute(sql,datos)
        cursor3.execute(sql2,datos2)
        cursor4.execute(sql3,_ID)
        datosREc = cursor4.fetchall()
        datosId = ((datosREc[0])[0])
        datosNombre = ((datosREc[0])[1])
        datosMarca = ((datosREc[0])[2])
        print(datosREc[0])
        datos = [{"idProducto": _ID, "nombre": _nombreProducto, "cantidad": _cantidad, "total": totalPag}]

        # conexionDB.close()

        titulo = "RECIBO"
        
        cabecera = (
            ("idProducto", "#"),
            ("nombre", "Nombre del producto"),
            ("cantidad", "Cantidad"),
            ("total", "Total"),
            )

        nombrePDF = "Proforma_de_venta.pdf"
        rep = reportePDF.reportePDF(titulo, cabecera, datos, nombrePDF,"Cliente:"+_Nom+" "+_Ap).Exportar()
        print(rep)
        conn.commit() 
        
        path = 'Proforma_de_venta.pdf'
        os.system(path)  
        # wb.open_new(r'C:\Proyecto\Pdf\Proforma_de_venta') 
        return redirect(url_for('busc'))
        

    # if _nombre=='' or _apellido=='' or _direccion=='' or _usuario=='' or _password=='' or _telefono=='' or _admin=='':
    #     flash('recuerda llenar los datos de todos los campos')
    #     return redirect(url_for('create'))
    # sql ="UPDATE empleado SET Nombre=%s, Apellido=%s, Telefono=%s, Direccion=%s, Usuario=%s, Password=%s, Admin=%s  WHERE idUsuarion=%s;"

@app.route('/historialVentas.html')
def method_name():
   return render_template('empleado/ventadatos.html')


@app.route("/cliente")
def cliente():

   sql = "SELECT * FROM `cliente`;"
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute(sql)
   clientes = cursor.fetchall()
   conn.commit()
   
   return render_template('empleado/cliente.html',clientes=clientes)


@app.route('/createCliente')
def createCliente():
   return render_template('empleado/createCliente.html')


@app.route('/storeCliente', methods=['POST'])
def storeCliente():
    _CI = request.form['txtCI']
    _Nombre = request.form['txtNombre']
    _Apellido = request.form['txtApellido']
    conn = mysql.connect()
    cursor1 =conn.cursor()
    cursor1.execute("SELECT CI FROM cliente where CI='"+ _CI +"'")
    info = cursor1.fetchall()
    print(info)
    if _Nombre=='' or _Apellido=='' or _CI=='':
        flash('recuerda llenar los datos de todos los campos')
        return redirect(url_for('createCliente'))
    if info != ():
        flash('El usuario ya existe')
        return redirect(url_for('createCliente'))

    sql ="INSERT INTO `cliente` (`CI`, `Nombre`, `Apellido` ) VALUES (%s, %s, %s);"
   

    datos=(_CI,_Nombre,_Apellido)
    
    cursor =conn.cursor()
    cursor.execute(sql,datos)
    print(cursor)
    conn.commit()
    return redirect('/cliente')


@app.route('/destroyCliente/<int:CI>')
def destroyCliente(CI):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente Where CI=%s",(CI))
    conn.commit()
    return redirect('/cliente')


@app.route('/edithCliente/<int:CI>')
def edithCliente(CI):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM cliente Where CI=%s", (CI))
    clientes=cursor.fetchall()
    # print(empleados)
    conn.commit()
    return render_template('empleado/edithCliente.html',clientes=clientes)

@app.route('/updateCliente', methods=['POST'])
def updateCliente():
   
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    id=request.form['txtID']
    sql ="UPDATE cliente SET Nombre=%s, Apellido=%s  WHERE CI=%s;"

    datos=(_nombre,_apellido,id)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/cliente')

@app.route("/historial")
def historial():

   sql = "SELECT * FROM `venta`;"
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute(sql)
   ventas = cursor.fetchall()
   conn.commit()
   
   return render_template('empleado/historialVentas.html',ventas=ventas)







if __name__ == '__main__':
    app.run(debug=True)