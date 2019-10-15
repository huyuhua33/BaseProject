import smtplib, ssl
import search
from email.mime.text import MIMEText
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "siganmorfu.testing@gmail.com"
receiver_email = "d0713227@mail.fcu.edu.tw"
password = "Stesting1121"
id='1540'
r=search.c_main(id)
ms = "the course u choice:"+search.c_name(r)+"\n"+"seat left: "+str(search.c_left(r))
head="U got a corse"

mime=MIMEText(ms, "plain", "utf-8")
mime["Subject"]="Gmail sent by Python scripts(MIME)"
mime["From"]="Your best friend"
mime["To"]="mailgroup"
msg=mime.as_string()


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted

    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg)

