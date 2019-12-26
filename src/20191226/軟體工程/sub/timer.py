# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:28:59 2019

@author: Jason
"""

import time
import sub.register


def timeUpdate(enable, registerhtml):
    t = time.time()
    while True:
        if stop_thread:
            return
        if enable:
            now = time.time()
            if (now - t) >= 30:
                sub.register.register(enable, registerhtml)
                t = time.time()
            elif (now - t) % 10:
                print("已經經過", int(now - t), "秒")
        else:
            return 0.0