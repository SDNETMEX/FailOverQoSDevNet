import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

usuario = "xxxxxxx@domain.com"
password = "password"
toaddr= ["xxxxxxx@domain.com","xxxxxxx@domain.com","xxxxxxx@domain.com", "xxxxxxx@domain.com","xxxxxxx@domain.com", "xxxxxxx@domain.com"]
toaddrrep= ["xxxxxxx@domain.com","xxxxxxx@domain.com","xxxxxxx@domain.com","xxxxxxx@domain.com"]
toaddcc = ["xxxxxxx@domain.com","xxxxxxx@domain.com"]

def send_email(asunto,cuerpo,dest_prin):
    try:

        conn = smtplib.SMTP('0.0.0.0',25)
        conn.ehlo()
#        conn.starttls()
#        conn.login(usuario, password)
        message = "From: " + usuario + "\r\n" + "To: emanuel.robledo@sdnet.com.mx, jose.gomez@megacable.com.mx\r\n" + "Subject: " + asunto + "\r\n" + "\r\n" + cuerpo
        print(message)
        conn.sendmail(usuario,["xxxxxxx@domain.com"],message)
        #conn.sendmail(usuario,["emanuel.robledo@sdnet.com.mx"],message)
        conn.quit()
        return 201
    except Exception as err:
        print(err)
        return 300

def send_email(asunto,cuerpo,dest_prin):
    try:

        conn = smtplib.SMTP('0.0.0.0',25)
        conn.ehlo()
#        conn.starttls()
#        conn.login(usuario, password)
        if dest_prin == "reporte":
            toaddress = toaddrrep
            message = "From: " + usuario + "\r\n" + "To: " + toaddress[0] + "\r\n" + "CC: " + toaddress[1] + ", " + toaddress[2] + ", " + toaddress[3] + "\r\n" + "Subject: " + asunto + "\r\n" + "\r\n" + cuerpo
        else:
            if dest_prin == "soporte":
                toaddress = toaddr[::-1]
            else:
                toaddress = toaddr
            message = "From: " + usuario + "\r\n" + "To: " + toaddress[0] + "\r\n" + "CC: " + toaddress[1] + ", " + \
                      toaddress[2] + ", " + toaddress[3] + ", " + toaddress[4] + ", " + toaddress[5] + "\r\n" + "Subject: " + asunto + "\r\n\r\n" + cuerpo
            #message = "From: " + usuario + "\r\n" + "To: emanuel.robledo@sdnet.com.mx\r\n" + "Subject: " + asunto + "\r\n" + cuerpo
        print(message)
        conn.sendmail(usuario,toaddress,message)
        #conn.sendmail(usuario,["emanuel.robledo@sdnet.com.mx"],message)
        conn.quit()
        return 201
    except Exception as err:
        print(err)
        return 300

def send_email_attachment(filename, asunto, mail_body):
    try:

        fromaddr = "xxxxxxx@domain.com"

        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = usuario

        # storing the receivers email address
        msg['To'] = "".join(toaddr)

        # storing the subject
        msg['Subject'] = asunto

        # attach the body with the msg instance
        msg.attach(MIMEText(mail_body, 'plain'))

        # open the file to be sent
        attachment = open("/var/www/FOyQoS/mail_excel/" + filename, 'rb')

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        msg['Cc'] = "".join(toaddcc)

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        # creates SMTP session
        conn = smtplib.SMTP('0.0.0.0',25)
        conn.ehlo()

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        conn.sendmail(fromaddr, toaddr, text)

        # terminating the session
        conn.quit()
        return 201

    except Exception as err:
        print(err)
        return "send_email " + str(err)
