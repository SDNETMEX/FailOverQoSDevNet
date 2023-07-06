import json, os
from get_bundle import show_interface
from shut_interface import shut_interface
from notificacion_correo import send_email
from get_bw import getBESpeed, getBETraffic
from timeStamp import get_timestamp_interval
from manage_mail_logs import write_mail_logs
from parse_alarm_desc import parse_alarm_desc

def Interface_Alarm(device,interface,desc):
    body_mail_alarm = parse_alarm_desc(desc)
    if "Discards" in desc:
        write_mail_logs(["Fail Over", device, interface, "Notificacion por Discards", desc])
        return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento discards , descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
    ### La parte de bundle no es usada actualmente, ya que se pidio que ni siquiera se notifique, por lo que se hace una validacion desde el script(alarm_received) que manda llamar este, y no se espera que entre a este if
    if "Bundle" in interface:
        print("La Interface es unica en la Bundle, no se puede apagar dicha interface")
        return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores, pero al ser Bundle, no se puede apagar dicha interface, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
        ### Notificar
    else:
        interface=interface.replace("\\","")
    bundle_info=show_interface(device, interface)
    print(bundle_info)
    if bundle_info == -1:
        print("Interface sin bundle")
        return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores, pero al no haber encontrado informacion acerca de a que bundle pertenece, no se procedera con su apagado, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
    if bundle_info!=400:
        if bundle_info!=0:
            time_intervals=get_timestamp_interval()
            print(time_intervals)
            bw_bundle=getBESpeed(device,bundle_info)
            print("Primera - " + str(bw_bundle))
            if "Gbps" in str(bw_bundle):
                print("Tiene gpbs" + bw_bundle)
                bw_bundle=int(bw_bundle.split(" ")[0])
            else:
                bw_bundle=bw_bundle/1000000000
            print(bw_bundle)
            traffic_bundle=getBETraffic(device,bundle_info,time_intervals[0],time_intervals[1])
            if traffic_bundle==400:
                print("No se pudo extraer el trafico anterior")
                return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores, pero no se pudo obtener el trafico del dia anterior para saber como proceder, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
                ### Notificar
            else:
                traffic_bundle=traffic_bundle/1000000000
            if "Ten" in interface:
                int_speed=10
                print(interface)
            elif "Hun" in interface:
                int_speed=100
            else:
                int_speed=1
            if bw_bundle-int_speed>traffic_bundle:
                print(str(bw_bundle)+" - "+str(int_speed)+" = "+str(bw_bundle-int_speed)+" > "+str(traffic_bundle))
                shut=shut_interface(device, interface)
                if shut !=400:
                    print("La Interface fue apagada exitosamente")
                    write_mail_logs(["Fail Over", device, interface, "Shutdown", desc])
                    return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores y fue apagada , la nueva configuracion seria la siguiente: \n " + shut + "\n descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
                else:
                    return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores pero no pudo ser apagada, si el problema persiste se llevara a cabo otro intento, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO", "soporte")
            else:
                print("El trafico maximo de la Bundle excede la banda ancha restante si se apaga la interfaz, por lo que se dejara encendida")
                return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores, pero el trafico maximo de la Bundle en la que se encuentra excede la banda ancha restante si se apaga la interfaz, por lo que se dejara encendida, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
        else:
            print("La Interface es unica en la Bundle, no se puede apagar dicha interface")
            write_mail_logs(["Fail Over", device, interface, "Ninguna: Interfaz unica en la bundle", desc])
            return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores, pero al ser unica en la Bundle, no se puede apagar dicha interface, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
            ### Notificar
    else:
        print("No se puede acceder")
        write_mail_logs(["Fail Over", device, interface, "Ninguna: No se pudo acceder al dispositivo", desc])
        return send_email("Notificacion Fail Over, Soporte", body_mail_alarm + "\nLa Interface: " + interface + " del dispositivo: " + device + " presento errores, pero no se pudo acceder al dispositivo para decidir como proceder, descripcion completa: \n " + desc + "   \n\n Atte. Cisco NSO","soporte")
        ### Notificar
