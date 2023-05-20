# -*- coding: utf-8 -*-
import requests
import json
from collections import defaultdict
from paddleocr import PaddleOCR
import logging
import re
import os, base64
import datetime
import time
import random
 
logging.disable(logging.DEBUG)
logging.disable(logging.WARNING)
prot = ["http://127.0.0.1:24401","http://127.0.0.1:24402","http://127.0.0.1:24403","http://127.0.0.1:24404","http://127.0.0.1:24405","http://127.0.0.1:24406","http://127.0.0.1:24407","http://127.0.0.1:24408","http://127.0.0.1:24409","http://127.0.0.1:24410"]
FILTER_PUNTS = re.compile('[^\u4E00-\u9FA5|^1-3]')
# 轻松识别验证码
class easyCode:
    def __init__(self):
        #self.ocr = PaddleOCR(use_angle_cls = True, use_gpu = True)
        self.ocr = PaddleOCR(enable_mkldnn=True, use_angle_cls=False, use_gpu = True, lang='ch') 

    def getPos(self, srcimg, keyimg)->int:
        try:
            keyList = self.getOcr(keyimg)
            if len(keyList) != 2:
                return 0
            return self.getRes(srcimg, keyList)
        except:
            print('except')
            return 0
        
    # ocr识别，获取个数和物品名称
    def getOcr(self, img) -> list:
        text=self.ocr.ocr(img, cls=True)#打开图片文件
        try:
            result = ''
            for val in text[0]:
                result = result + val[1][0]
            result = result.replace('众','个')
            result = result.replace('人','个')
            result = result.replace('八','个')
            result = FILTER_PUNTS.sub('', result.strip())
            if result == '':
                return []
            else:
                result = result.split('个')
                if result[0] == '' or result[0] > '3':
                    result[0] = '1'
                return result
        except:
            return []

    # 返回目标位置：相对大图的最右边坐标，识别识别则返回值为0
    def getRes(self, img, ocrList)->int:
        try:
            with open(img, 'rb') as f:
                img = f.read()
            target = defaultdict(list)
            ## params 为GET参数 data 为POST Body
            url1=prot[random.randint(0,9)]
            result = json.loads(requests.post(url="http://127.0.0.1:24401", params={'threshold': 0.5}, data=img).content)
            if result['error_code'] == 0:
                for small in result['results']:
                    target[small['label']].append(small['location']['left'] + small['location']['width'])
                for val in target.values():
                    val.sort()
                if len(target[ocrList[1]]) >= int(ocrList[0]):
                    return target[ocrList[1]][int(ocrList[0]) - 1]
            else:
                return 0
        except:
            return 0

if __name__=='__main__':
    start = time.perf_counter()
    verifyCode  = easyCode()
    print('init:',time.perf_counter() - start)
    #print(verifyCode.getRes('../../image/1_123/3yzimg.png',['2','玫瑰花']))
    # with open('../../image/1_123/3yzimg.png', 'rb') as src:
    #     srcData = base64.b64encode(src.read())
    #     print(srcData)
    #     with open('../../image/122/3tsimg.png', 'rb') as key:
    #         keyData = base64.b64encode(key.read())
    #         print(keyData)
    #         print(verifyCode.getPos(srcData, keyData))
    # print('end:',time.perf_counter() - start)
    
    