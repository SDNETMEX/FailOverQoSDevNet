import os
from manage_json import GetJson, WriteJson
import base64
import rsa

def Get_Current_Values():
    files = os.listdir('/var/www/FOyQoS/JsonFiles/')
    jsondev = {}

    for file in files:
        if "Known_Hosts" not in file and "Logs" not in file and "max_values" not in file and "users" not in file:
            json = GetJson(file.replace(".json", ""))
            men_cambios = ""
            for queue in json[file.replace(".json", "")]:
                if json[file.replace(".json", "")][queue] > 0:
                    men_cambios = men_cambios+queue+": %" + \
                        str(json[file.replace(".json", "")][queue])+". "
                if men_cambios != "":
                    jsondev[file.replace(".json", "")] = [
                        men_cambios, json["intentos"]]
                    # jsondev[file.replace(".json","")][0]=men_cambios
                    # jsondev[file.replace(".json","")][1]=json["intentos"]
    return jsondev


def Rollback(hostname):
    # json_val=get_policy_map(hostname)
    json_host = GetJson(hostname)
    json_host["intentos"] = 0
    WriteJson(json_host, hostname)
    return "Rollback Reagendado"


def Get_Devices():
    files = os.listdir('/var/www/FOyQoS/JsonFiles/')
    arrdev = []
    for file in files:
        if "Known_Hosts" not in file and "Logs" not in file and "max_values" not in file and "users" not in file:
            json = GetJson(file.replace(".json", ""))
            if json["intentos"] < 3:
                for queue in json[file.replace(".json", "")]:
                    if json[file.replace(".json", "")][queue] > 0:
                        arrdev.append(file.replace(".json", ""))
                        print(arrdev)
                        break

    return arrdev


def Get_Logs():
    json = GetJson("Logs")
    return json


def Get_Logs_Filtered(fecha_hora):
    json = GetJson("Logs")
    fecha = fecha_hora.split('T')[0]
    print(fecha)
    fil_json = {}
    for key in json:
        if fecha in key:
            fil_json[key] = json[key]
    return fil_json


def Get_Users():
    json = GetJson("users")
    return json


def Change_User(accion, user, new_user):
    json = GetJson("users")
    if accion == "Eliminar":
        json["Users"].remove(user)
    elif accion == "Modificar":
        if user == new_user:
            return "Ingrese un nuevo nombre de usuario"
        else:
            json["Users"].remove(user)
            json["Users"].append(new_user)
    else:
        if new_user in json["Users"]:
            return "El usuario que se desea agregar ya existe"
        else:
            json["Users"].append(new_user)
    wrt = WriteJson(json, "users")
    return wrt


def Get_Queues():
    json = GetJson("max_values")
    return json


def Change_Queue(queue, min_val, max_val, accion):
    json = GetJson("max_values")
    min_tot = 0
    if accion == "Eliminar":
        json.pop(queue)
    else:
        for x in json:
            print(x + queue)
            if x != "Maximo-Total":
                if x != queue:
                    min_tot += int(json[x][0])
        print(min_tot)
        if (min_tot+min_val) > int(json["Maximo-Total"][0]) and queue != "Maximo-Total":
            return "El valor especificado no puede ser configurado ya que superaria el minimo total permitido"
        elif queue == "Maximo-Total":
            print("entre")
            if min_val < min_tot and min_val != 0:
                return "El valor total minimo de las queue no puede ser menor que la suma de los valores minimos de las demas queues"
            elif max_val > 95:
                return "El valor total maximo de las queue no puede ser mayor que 95"
        if max_val == 0:
            if min_val < int(json[queue][1]):
                json[queue][0] = min_val
            else:
                return "El limite inferior no puede superar al mayor"
        elif min_val == 0:
            if max_val > int(json[queue][0]):
                json[queue][1] = max_val
            else:
                return "El limite superior no puede ser menor que el inferior"
        else:
            json[queue] = [min_val, max_val]
    wrt = WriteJson(json, "max_values")
    return wrt


def decrypt_string(encrypted_string):

    encrypted_message = base64.b64decode(encrypted_string.encode('utf-8'))

    # Cambiar direccion y archivo de la private key
    with open('/var/www/pvtkey.pem', mode='rb') as privatefile:
        keydata = privatefile.read()

    pvtkey = rsa.PrivateKey.load_pkcs1(keydata)

    message = rsa.decrypt(encrypted_message, pvtkey)

    return message.decode('utf8')