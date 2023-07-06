# Import requests library
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import os
from flask import Flask, request, flash, redirect, url_for
from flask import render_template, jsonify, flash
from flask_cors import CORS
from tacacs_plus.client import TACACSClient
from manage_mail_logs import get_mail_logs
from main_services import Get_Current_Values, Rollback, Get_Devices, Get_Logs, Get_Logs_Filtered, Get_Queues, Change_Queue, Get_Users, Change_User, decrypt_string

# Intialize a web app
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ['secret']
ip_nso = os.environ['IP_NSO']
tacacs_master = os.environ['tacacs_master']
tacacs_backup = os.environ['tacacs_backup']

@app.route("/")
def index():
    return render_template("Login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    jsonusers = Get_Users()
    user = request.form["user"]
    pswrd = request.form["password"]
    pswrd = decrypt_string(pswrd)

    if user in jsonusers["Users"]:
        # return render_template("Menu.html")
        try:
            auth = TACACSClient(
                tacacs_master, 49, 'pre_post_development', timeout=40).authenticate(user, pswrd)
        except Exception as err:
            auth = TACACSClient(
                tacacs_backup, 49, 'pre_post_development', timeout=40).authenticate(user, pswrd)
        if auth.valid:
            return render_template("Menu.html")
        else:
            flash("Credenciales incorrectas", "warning")
    else:
        flash("Usuario no registrado en el desarrollo", "warning")

    return render_template("Login.html")


@app.route('/menu_principal')
def menu_principal():
    return render_template("Menu.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/con_rollback', methods=['GET', 'POST'])
def con_rollback():
    """if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)"""
    jsondev = Get_Current_Values()
    print(jsondev)
    if jsondev == {}:
        # Si no encontró ningún dispositivo con cambios muestra un mensaje diciéndolo
        flash("No hay dispositivos con cambios realizados actualmente", "success")
    else:
        # Ordena los dispositivos poniendo primero a los que tienen 3 intentos, la primera línea regresa un arreglo de tuplas, y la siguiente lo devuelve a diccionario
        ordered_dev_tuple = sorted(
            jsondev.items(), key=lambda x: x[1][1], reverse=True)
        jsondev = {i[0]: [i[1][0], i[1][1]] for i in ordered_dev_tuple}
    return render_template("rollback.html", devices=jsondev)


@app.route('/update_rollback', methods=['GET', 'POST'])
def update_rollback():
    device = request.form["submit_button"]
    print(device)
    roll = Rollback(device)
    jsondev = Get_Current_Values()
    return render_template("rollback.html", devices=jsondev)


@app.route('/manage_queue', methods=['GET', 'POST'])
def manage_queue():
    jsonq = Get_Queues()
    return render_template("manage_queue.html", queues=jsonq)


@app.route('/changes_queue', methods=['GET', 'POST'])
def changes_queue():
    accion = request.form["name_service"]
    filt = 1
    min_val = 0
    max_val = 0
    if accion == "Agregar":
        nombre = request.form["nombre_queue"]
        max_val = request.form["max_val"]
        min_val = request.form["min_val"]
        if not nombre or not max_val or not min_val:
            filt = 0
            flash("Asegurese de ingresar todos los campos", "warning")
        elif int(min_val) > int(max_val):
            flash("El limite inferior no puede rebasar el superior", "warning")
            filt = 0
    elif accion == "Modificar":
        nombre = request.form["sel_queue"]
        limite = request.form["limites"]
        if nombre == "Seleccione una Queue":
            flash("Asegurese de ingresar todos los campos", "warning")
            filt = 0
        elif limite == "Máximo":
            max_val = request.form["max_val"]
        else:
            min_val = request.form["min_val"]
        if min_val == "" or max_val == "" or (int(min_val) == 0 and int(max_val) == 0):
            filt = 0
            flash("Asegurese de ingresar todos los campos", "warning")
    elif accion == "Eliminar":
        nombre = request.form["sel_queue"]
        if nombre == "Maximo-Total":
            flash("El maximo total no puede ser borrado", "warning")
            filt = 0
    if filt == 1:
        chng = Change_Queue(nombre, int(min_val), int(max_val), accion)
        print(chng)
        if chng == 200:
            flash("Queue actualizada correctamente", "success")
        else:
            flash(chng, "warning")
    jsonq = Get_Queues()
    return render_template("manage_queue.html", queues=jsonq)


@app.route('/devices_logs', methods=['GET', 'POST'])
def devices_logs():
    logs = Get_Logs()
    print(logs)
    return render_template("logs_page.html", logs=logs)


@app.route('/filter_logs', methods=['GET', 'POST'])
def filter_logs():
    fecha = request.form["fecha_hora"]
    print(fecha)
    logs = Get_Logs_Filtered(fecha)
    if logs == {}:
        # Si no encuentra logs de esa fecha muestra un mensaje
        flash("No hay cambios registrados en la fecha seleccionada", "warning")
    else:
        print(logs)
    return render_template("logs_page.html", logs=logs, fecha_hora=fecha)


@app.route('/mail_logs', methods=['GET', 'POST'])
def mail_logs():
    fecha = str(datetime.now())
    logs = get_mail_logs(fecha[0:10])
    print(fecha)
    print(logs)
    if logs == {}:
        # Si no encuentra logs de esa fecha muestra un mensaje
        flash("No hay correos mandados en la fecha seleccionada", "warning")
        return render_template("mail_logs.html", fecha_hora=fecha[0:10])
    else:
        print(logs)
        return render_template("mail_logs.html", logs=logs, fecha_hora=fecha[0:10])


@app.route('/filter_mail_logs', methods=['GET', 'POST'])
def filter_mail_logs():
    fecha = request.form["fecha_hora"]
    print(fecha)
    logs = get_mail_logs(fecha.split('T')[0])
    print(logs)
    if logs == {}:
        # Si no encuentra logs de esa fecha muestra un mensaje
        flash("No hay correos mandados en la fecha seleccionada", "warning")
        return render_template("mail_logs.html", fecha_hora=fecha[0:10])
    else:
        print(logs)
        return render_template("mail_logs.html", logs=logs, fecha_hora=fecha[0:10])


@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    jsonusers = Get_Users()
    return render_template("manage_users.html", users=jsonusers)


@app.route('/changes_user', methods=['GET', 'POST'])
def changes_user():
    accion = request.form["name_service"]
    filt = 1
    sel_nombre = ""
    nombre = ""
    if accion == "Agregar":
        nombre = request.form["nombre_user"]
        if not nombre:
            flash("Ingrese el nombre de usuario", "warning")
            filt = 0
    elif accion == "Modificar":
        sel_nombre = request.form["sel_user"]
        nombre = request.form["nombre_user"]
        if sel_nombre == "Seleccione un Usuario" or not nombre:
            flash("Asegurese de ingresar todos los campos", "warning")
            filt = 0
    else:
        sel_nombre = request.form["sel_user"]
        if sel_nombre == "Seleccione un Usuario":
            flash("Seleccione el usuario que desea eliminar", "warning")
            filt = 0
    if filt == 1:
        chng = Change_User(accion, sel_nombre, nombre)
        print(chng)
        if chng == 200:
            flash("Lista de usuarios actualizada correctamente", "success")
        else:
            flash(chng, "warning")
    jsonusers = Get_Users()
    return render_template("manage_users.html", users=jsonusers)


@app.route('/api/lldp-service-devices/<serviceid>',  methods=['POST', 'GET'])
def lldp_service_device(serviceid):
    r = requests.get("http://" + ip_nso + ":8080/restconf/data/tailf-ncs:services/vlans-lldp:vlans-lldp="+serviceid,
                     headers={'Accept': 'application/yang-data+json'},
                     auth=HTTPBasicAuth("admin", "admin"))
    result = r.json()
    return result


@app.route('/api/service-dryrun/<service>',  methods=['POST', 'GET'])
def service_dryrun(service):
    dry_run = get_dry_run(service)
    print(dry_run)
    return dry_run


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
