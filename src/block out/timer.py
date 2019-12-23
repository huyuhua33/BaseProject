import time


def timeUpdate(enable, initial=0.0):
    if enable:
        now = time.time()
        if now - initial >= 300:
            register(enable, registHtml)
        else:
            return initial
    else:
        return 0.0
