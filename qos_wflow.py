from datetime import datetime
from get_policy_map import get_policy_map
from manage_json import GetJson, WriteJson
from elevar_porcentaje import elevar_porcentaje
from notificacion_correo import send_email
from manage_mail_logs import write_mail_logs
from parse_alarm_desc import parse_alarm_desc

def DeviceAlarm(hostname, queue, desc):
    body_mail_alarm = parse_alarm_desc(desc)
    json=get_policy_map(hostname)
    print(json)
    limite=ComprobarLimite(hostname,json,queue)
    print(limite)
    if limite == 1:
        mensaje = ElevarPorcentaje(hostname,json,queue,desc)
        print(mensaje)
        if mensaje != 400:
            prueba_correo_status = send_email("Notificacion QoS, Operacion", body_mail_alarm + "\nLa queue: " + queue + " del dispositivo" + hostname + " esta presentando drops, se elevo 1% su espacio reservado, el dryrun de la configuracion es el siguiente: \n" + mensaje + "\n descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","operacion")
        else:
            prueba_correo_status = send_email("Notificacion QoS, Operacion", body_mail_alarm + "\nLa queue: " + queue + " del dispositivo" + hostname + " esta presentando drops, se intento elevar 1% su espacio reservado pero la API fallo, si el problema persiste se hara un nuevo intento, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","operacion")
    elif limite == 0:
        mensaje="Max total alcanzado"
        prueba_correo_status = send_email("Notificacion QoS, Soporte", body_mail_alarm + "\nEl maximo espacio reservado para QoS del dispositivo: " + hostname + " ya fue alcanzado, pero sigue presentando drops, por lo que ya no se elevara el porcentaje en ninguna queue, descripcion completa: \n " + desc + "  \n\n Atte. Cisco NSO","soporte")
        write_mail_logs(["QoS", hostname, queue, "Notificacion: Maximo total alcanzado", desc])
    elif limite == 2:
        mensaje="Queue no prioritaria"
        prueba_correo_status = send_email("Notificacion QoS, Soporte", body_mail_alarm + "\nLa Queue " + queue + " del dispositivo: " + hostname + " esta teniendo drops, pero al no ser cola prioritaria, no se elevara su porcentaje, descripcion completa: \n " + desc + "  \n\n Atte. Cisco NSO","soporte")
        write_mail_logs(["QoS", hostname, queue, "Notificacion: Queue no prioritaria", desc])
    elif type(limite) == str:
        prueba_correo_status = send_email("Notificacion QoS, Operacion", body_mail_alarm + "\nLa Queue " + limite + " del dispositivo: " + hostname + " no se encuentra en nuestros registros para verificar si excedio su valor maximo, por lo que no realizaremos ninguna accion, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","operacion")
        write_mail_logs(["QoS", hostname, queue, "Notificacion: La Queue no tiene un valor maximo definido", desc])
        mensaje = limite + " desconocida"
    else:
        prueba_correo_status = send_email("Notificacion QoS, Soporte", body_mail_alarm + "\nLa Queue " + limite[0] + " del dispositivo: " + hostname + " esta teniendo drops, pero su porcentaje maximo  " + limite[1] + "  ya fue alcanzado y no se puede incrementar mas, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
        write_mail_logs(["QoS", hostname, queue, "Notificacion: El valor maximo de queue " + limite[1] + "  ya fue alcanzado", desc])
        mensaje = "La Queue " + limite[0] + " del dispositivo: " + hostname + " esta teniendo drops, pero su porcentaje maximo  " + limite[1] + "  ya fue alcanzado"
    return mensaje

def ComprobarLimite(hostname,jsonqueue,queue):
    ###Este json tambien puede ser omitido una vez en produccion
    json=GetJson(hostname)
    print(json)
    json_lim=GetJson("max_values")
    prcnttot=0
    for key_queue in jsonqueue:
        prcnttot+=jsonqueue[key_queue]
    print(prcnttot)
    try:
        valor_queue_disp = int(jsonqueue[queue])
    except Exception as err:
        print(err)
        return 2
    if prcnttot>=int(json_lim["Maximo-Total"][1]):
        ###Notificacion por el medio que se decida
        return 0
    else:
        try:
            if valor_queue_disp>=int(json_lim[queue][1]):
                return [queue,json_lim[queue][1]]
        except Exception as err:
            print(err)
            return queue
        return 1

def ElevarPorcentaje(hostname,json,queue,desc):
    jsonqueue = GetJson(hostname)
    jsonlogs = GetJson("Logs")
    if jsonqueue==0:
        jsonqueue={}
        jsonqueue["intentos"]=0
        jsonqueue[hostname]={}
        for key_queue in json:
            jsonqueue[hostname][key_queue]=0
    porcentaje=str(json[queue]+1)
    request = elevar_porcentaje(hostname,queue,porcentaje)
    if request != 400:
        porcentaje_avance = str(json[queue]) + " - " + porcentaje
        jsonqueue[hostname][queue]=jsonqueue[hostname][queue]+1
        if jsonlogs == 0:
            jsonlogs={}
        fecha=str(datetime.now())
        jsonlogs[fecha]=[hostname,queue,porcentaje_avance]
        write_mail_logs(["QoS",hostname,queue,"Configuracion porcentaje: " + porcentaje_avance, desc])
        WriteJson(jsonqueue,hostname)
        WriteJson(jsonlogs, "Logs")
        return(request)
    else:
        return 400
