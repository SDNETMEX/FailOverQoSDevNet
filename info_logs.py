from datetime import datetime
import os

def info_logs(log):
    if not os.path.exists('info_logs'):
        os.mkdir('info_logs')
    date=datetime.now()
    f=open("info_logs/" + str(date)[0:10]+ ".txt", "a+")
    f.write("\n*********************************************************\n")
    f.write((str(date))[11:19] +"  ---  " + log + "\n")
    f.close()
    return "Log guardado exitosamente"