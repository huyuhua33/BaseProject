import smtplib, ssl
import sub.search as search
from email.mime.text import MIMEText


def mail(receiver_email, sw, randword, id):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "siganmorfu.testing@gmail.com"
    # receiver_email = "d0713227@mail.fcu.edu.tw"
    password = "Stesting1121"
    if (sw == 1):
        r = search.c_main(id,'108','1')

        try:
            c=search.c_left(r)
        except:
            return -1
        if (c <= 0):
            print("now waiting")
            while (c <= 0):
             c = search.c_left(r)
        print("Finish!")
        name = search.c_name(r)
        c = str(search.c_left(r))
        ms = "the course u choice:" + name + "\n" + "seat left: " + c
        # head="U got a corse"
        mime = MIMEText(ms, "plain", "utf-8")
        mime["Subject"] = "課程剩餘通知:"+ name
        mime["From"] = "搶課無極限"
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
    return 0
