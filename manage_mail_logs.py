import json
from datetime import datetime
from parse_alarm_desc import parse_alarm_desc_to_mail_logs_table


def get_mail_logs1(fecha):
    try:
        with open('/var/www/FailOverQoSDevNet/mail_json/' + fecha + '.json') as json_file:
            data = json.load(json_file)
        return data
    except:
        return {}

def get_mail_logs(fecha):
    try:
        with open('/var/www/FailOverQoSDevNet/mail_json/'+fecha+'.json') as json_file:
            data = json.load(json_file)

        for log in data:
            parsed_fields = parse_alarm_desc_to_mail_logs_table(data[log][4])
            new_row = [data[log][0]]
            new_row += parsed_fields
            new_row.append(data[log][3])
            ### Formato orden de campos: Caso, Dispositivo, Interfaz, Error, Medida, Valor, Condicion, Class Map, Queue, Direccion, Accion
            data[log] = new_row
        return data
    except:
        return {}


def write_mail_logs(log_details):
    fecha = str(datetime.now())
    try:
        with open('/var/www/FailOverQoSDevNet/mail_json/'+fecha[0:10]+'.json') as json_file:
            json_fecha = json.load(json_file)
    except:
        json_fecha = {}
    if json_fecha != 400:
        json_fecha[fecha]=log_details
        with open('/var/www/FailOverQoSDevNet/mail_json/'+fecha[0:10]+'.json', 'w') as outfile:
            json.dump(json_fecha, outfile)
        return 200
    else:
        return 400
