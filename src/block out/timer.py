import time


def timeUpdate(initial=0.0):
    now = time.time()
    if now - initial >= 300:
        regist(registHtml)
    else:
        return initial
