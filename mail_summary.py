#!/usr/bin/python3

from datetime import datetime
from manage_mail_logs import get_mail_logs1
from notificacion_correo import send_email_attachment
from crear_reporte_excel import crear_reporte_excel

def mail_summary(fecha):
    json_fecha = get_mail_logs1(fecha)
    mail_body = "Fecha,Caso,Accion,Alarma,Error,Medida,Valor,Condicion,Equipo,Interface,Class Map,Cola,Direccion\n"
    excel_table = []
    row_excel = mail_body.replace("\n","").split(",")
    excel_table.append(row_excel)
    for correo in json_fecha:
        descripcion_completa = json_fecha[correo][4]
        mail_line = correo.split(".")[0] + "," + json_fecha[correo][0] + "," + json_fecha[correo][3].replace(",",":") + ","
        alarma = descripcion_completa.split("Additional Details")[0].split("\".")[1].strip()[:-1]
        addiotional_details=descripcion_completa.split("Additional Details")[1]
        arr_error = alarma.split("Rate")
        if len(arr_error) > 1:
            medida = "Rate"
            error_c = arr_error[0].strip()
        else:
            medida = "Percentage"
            error_c = alarma.split("Percentage")[0].strip()
        valor = alarma.split("value")[1].split("is")[0].strip()
        arr_additional_details = addiotional_details.split(";")
        condicion = arr_additional_details[1].split(":")[1].strip()
        arr_interface = arr_additional_details[2].split(":")[1].split("/", 1)
        dispositivo = arr_interface[0].split(".")[0].strip()
        interface = arr_interface[1].replace(".","").strip()
        if json_fecha[correo][0] == "QoS":
            arr_classmap = arr_additional_details[3].split(":")
            class_map = arr_classmap[1].strip()
            cola = arr_classmap[2].strip()
            direccion = arr_additional_details[4].split(":")[1].replace(".","").strip()
        else:
            class_map = "N/A"
            cola = "N/A"
            direccion = "N/A"

        mail_line = mail_line + alarma + "," + error_c + "," + medida + "," + valor + "," + condicion + "," + dispositivo + "," + interface + "," + class_map + "," + cola + "," + direccion + "\n"
        mail_body = mail_body + mail_line
        row_excel = mail_line.replace("\n", "").split(",")
        excel_table.append(row_excel)

    filename = fecha+"_reporte.xlsx"
    crear_reporte_excel(excel_table, filename)

    return send_email_attachment(filename, "Alarmas RAC","A continuacion se muestran los correos enviados a lo largo del dia " + fecha + "\n\n" + mail_body)


fecha = str(datetime.now())
print(mail_summary(fecha[0:10]))