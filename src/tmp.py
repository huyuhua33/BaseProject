import smtplib
from email.mime.text import MIMEText

mime=MIMEText("您好! 我是 Tony.", "plain", "utf-8")
mime["Subject"]="Gmail sent by Python scripts(MIME)"
mime["From"]="Your best friend"
mime["To"]="mailgroup"
mime["Cc"]="myyahoomail@yahoo.com, mycompanymail@blablabla.com.tw"
msg=mime.as_string()

smtp=smtplib.SMTP("smtp.gmail.com", 587)
smtp.ehlo()
smtp.starttls()
smtp.login("siganmorfu.testing@gmail.com", "Stesting1121")
from_addr="siganmorfu.testing@gmail.com"
to_addr=["hu881121@gmail.com"]
status=smtp.sendmail(from_addr, to_addr, msg)
if status=={}:
    print("郵件傳送成功!")
else:
    print("郵件傳送失敗!")
smtp.quit()