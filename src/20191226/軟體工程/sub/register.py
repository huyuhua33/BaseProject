# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:27:22 2019

@author: Jason
"""
courseIDs = ['0718', '0719', '2020', '2027', '1255']


def register(enable, registHtml, courseID='0000'):
    if enable == 1:
        if courseID == '0000':
            print("超過系統時限，已發送刷新指令")
        else:
            for i in courseIDs:
                if i == courseID:
                    print("加選成功")
                    courseIDs.remove(courseID)
                    break