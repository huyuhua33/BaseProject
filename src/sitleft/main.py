import sub.mailing as mailing
def send(email):
    ID = input("ID>>")
    r = mailing.mail(email, 1, 0, ID)
    while (r == -1):
        print("輸入錯誤")
        ID = input("ID>>")
        r = mailing.mail(email, 1, 0, ID)
    return 0
email  = input()
send(email)
