from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://estudiante:123456@localhost/guarderia'
app.config['SECRET_KEY'] = '974d073af26164ac9d7aa7d206dd4e94'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100), unique=True)
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(255))
    tipo_usuario = db.Column(db.String(50))
    password = db.Column(db.String(128)) 

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    raza = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    peso = db.Column(db.Numeric(5, 2))
    alergias = db.Column(db.Text)
    vacunas = db.Column(db.Text)
    dueño_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Guarderia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    ubicacion = db.Column(db.String(255))


class ReservaServicio(db.Model):
    __tablename__ = 'reserva_servicio'
    reserva_id = db.Column(db.Integer, db.ForeignKey('reserva.id'), primary_key=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), primary_key=True)

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    reservas = db.relationship('Reserva', secondary='reserva_servicio', back_populates='servicios')

class Reserva(db.Model):
    __tablename__ = 'reserva'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    estado = db.Column(db.String(50))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'))
    guarderia_id = db.Column(db.Integer, db.ForeignKey('guarderia.id'))
    servicios = db.relationship('Servicio', secondary='reserva_servicio', back_populates='reservas')


class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Numeric(10, 2))
    fecha = db.Column(db.Date)
    metodo_pago = db.Column(db.String(50))
    reserva_id = db.Column(db.Integer, db.ForeignKey('reserva.id'))

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        password = request.form['password']  # Obtener contraseña del formulario

        # Crear nuevo usuario
        new_user = Usuario(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            password=generate_password_hash(password)  # Hashear la contraseña
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirigir al login después del registro

    return render_template('register_user.html')


@app.route('/register_dog', methods=['GET', 'POST'])
@login_required
def register_dog():
    mensaje = None  # Variable para el mensaje

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        raza = request.form['raza']
        edad = request.form['edad']
        peso = request.form['peso']
        alergias = request.form.get('alergias', '')
        vacunas = request.form.get('vacunas', '')
        dueño_id = current_user.id  # Asumiendo que el dueño es el usuario actual

        # Verificar si la mascota ya existe
        mascota_existente = Mascota.query.filter_by(nombre=nombre, dueño_id=dueño_id).first()
        if mascota_existente:
            mensaje = 'Ya existe una mascota con ese nombre. Por favor, elige otro nombre.'
        else:
            # Crear nueva mascota
            nueva_mascota = Mascota(
                nombre=nombre,
                raza=raza,
                edad=edad,
                peso=peso,
                alergias=alergias,
                vacunas=vacunas,
                dueño_id=dueño_id
            )
            db.session.add(nueva_mascota)
            db.session.commit()
            mensaje = 'Mascota registrada exitosamente!'  # Mensaje de éxito

    return render_template('register_dog.html', mensaje=mensaje)


@app.route('/reserve_service', methods=['GET', 'POST'])
@login_required
def reserve_service():
    mascotas = Mascota.query.filter_by(dueño_id=current_user.id).all()
    guarderias = Guarderia.query.all()
    servicios = Servicio.query.all()

    if request.method == 'POST':
        # Obtener las fechas seleccionadas
        fechas = request.form['fechas'].split(',')  # Suponiendo que vienen en un string separado por comas
        
        nueva_reserva = Reserva(
            estado='Pendiente',
            mascota_id=request.form['mascota_id'],
            guarderia_id=request.form['guarderia_id']
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        servicios_seleccionados = request.form.getlist('tipo_servicio')
        for servicio_id in servicios_seleccionados:
            servicio = Servicio.query.get(servicio_id)
            if servicio:
                nueva_reserva.servicios.append(servicio)

        db.session.commit()

        # Redirigir a la vista de pago con el monto y las fechas
        return redirect(url_for('pago', reserva_id=nueva_reserva.id, fechas=','.join(fechas)))

    return render_template('reserve_service.html', mascotas=mascotas, guarderias=guarderias, servicios=servicios)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        user = Usuario.query.filter_by(correo=correo).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso!', 'success')  # Mensaje de éxito
            return redirect(url_for('index'))

        flash('Credenciales incorrectas', 'danger')  # Mensaje de error

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')  # Mensaje de información
    return redirect(url_for('index'))

def calcular_monto_reserva(reserva, fechas):
    # Calcular la cantidad de días seleccionados
    cantidad_dias = len(fechas)  # Contar las fechas seleccionadas
    monto = 0.0

    for servicio in reserva.servicios:
        # Definir el costo por servicio
        if servicio.nombre == "Cuidado diario y alojamiento para perros":
            monto += 100000
        elif servicio.nombre == "Entrenamiento y socialización":
            monto += 50000
        elif servicio.nombre == "Paseos y actividades recreativas":
            monto += 30000
        elif servicio.nombre == "Servicios de grooming y spa":
            monto += 50000
        elif servicio.nombre == "Asesoría para dueños de mascotas":
            monto += 40000

    # Multiplicar el monto total por la cantidad de días
    return monto * cantidad_dias



@app.route('/pago/<int:reserva_id>', methods=['GET'])
@login_required
def pago(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if reserva is None:
        flash('Reserva no encontrada', 'danger')
        return redirect(url_for('index'))

    # Obtenemos las fechas seleccionadas del query string
    fechas = request.args.get('fechas')
    if fechas is None:
        flash('No se encontraron fechas seleccionadas', 'danger')
        return redirect(url_for('index'))
    
    fechas = fechas.split(',')

    # Calcular el monto utilizando las fechas seleccionadas
    monto = calcular_monto_reserva(reserva, fechas)

    return render_template('pagos.html', monto=monto, reserva_id=reserva_id)


@app.route('/realizar_pago/<int:reserva_id>', methods=['POST'])
@login_required
def realizar_pago(reserva_id):
    metodo_pago = request.form['metodo_pago']
    monto = request.form.get('monto')
    fecha = datetime.now().date()

    nuevo_pago = Pago(
        monto=monto,
        fecha=fecha,
        metodo_pago=metodo_pago,
        reserva_id=reserva_id
    )
    db.session.add(nuevo_pago)
    db.session.commit()
    
    flash('Pago realizado exitosamente!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
