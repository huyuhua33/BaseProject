import smtplib, ssl
import sub.search as search
from email.mime.text import MIMEText
senderUser =""
senderPass = ""

def mail(receiver_email, sw, randword, id):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = senderUser
    # receiver_email = "d0713227@mail.fcu.edu.tw"
    password = senderPass
    if (sw == 1):
        r = search.c_main(id)
        ms = "the course u choice:" + search.c_name(r) + "\n" + "seat left: " + str(search.c_left(r))
        # head="U got a corse"
        mime = MIMEText(ms, "plain", "utf-8")
        mime["Subject"] = "Gmail sent by Python scripts(MIME)"
        mime["From"] = "Your best friend"
        mime["To"] = "mailgroup"
    else:
        ms = str(randword)
        mime = MIMEText(ms, "plain", "utf-8")
        mime["Subject"] = "Veratify ID"
        mime["From"] = "驗證碼"
        mime["To"] = "mailgroup"

    msg = mime.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted

        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)
