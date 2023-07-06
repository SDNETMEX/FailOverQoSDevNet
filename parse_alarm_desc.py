from datetime import datetime

def parse_alarm_desc(descripcion_completa):
    alarma = descripcion_completa.split("Additional Details")[0].split("\".")[1].strip()[:-1]
    addiotional_details = descripcion_completa.split("Additional Details")[1]
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
    interface = arr_interface[1].replace(".", "").strip()
    body_structure = "Interface: " + interface + "\n"\
                     "Equipo: " + dispositivo + "\n"\
                     "Alarma: " + alarma + "\n"\
                     "Error: " + error_c + "\n"\
                     "Medida: " + medida + "\n"\
                     "Valor: " + valor + "\n"\
                     "Condicion: " + condicion + "\n"
    if "QoSAlarm" in descripcion_completa:
        arr_classmap = arr_additional_details[3].split(":")
        class_map = arr_classmap[1].strip()
        cola = arr_classmap[2].strip()
        direccion = arr_additional_details[4].split(":")[1].replace(".", "").strip()
        body_structure = body_structure + "Class Map: " + class_map + "\n" + "Cola: "\
                                        + cola + "\n" + "Direccion: " + direccion + "\n"

    body_structure = body_structure + "Fecha: " + str(datetime.now()).split(".")[0] + "\n"

    return body_structure


def parse_alarm_desc_to_mail_logs_table(descripcion_completa):
    alarma = descripcion_completa.split("Additional Details")[0].split("\".")[1].strip()[:-1]
    addiotional_details = descripcion_completa.split("Additional Details")[1]
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
    interface = arr_interface[1].replace(".", "").strip()
    response_array = [dispositivo, interface, error_c, medida, valor,condicion]
    if "QoSAlarm" in descripcion_completa:
        arr_classmap = arr_additional_details[3].split(":")
        class_map = arr_classmap[1].strip()
        cola = arr_classmap[2].strip()
        direccion = arr_additional_details[4].split(":")[1].replace(".", "").strip()
        response_array += [class_map, cola, direccion]
    else:
        response_array += ["N/A","N/A","N/A"]

    return response_array