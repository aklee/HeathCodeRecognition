import pytesseract
from PIL import Image
# from openpyxl.drawing.image import Image
import os
import shutil
import re
from enum import Enum

class CardType(Enum):
    HealthCard = 1,
    TravalCard = 2,
    UnknownCard = 9

class HeathCodeRecognition:
    def __init__(self, path):
        self.path = path
        self.imglist = []
        self.resultlist = []

    def findFile(self):
        items = os.listdir(self.path)
        subfixs = ['.png','.jpg','.jpeg']
        imglist = []
        for item in items:
            filePath = os.path.join(self.path, item)
            if os.path.isfile(filePath):
                if os.path.splitext(filePath)[1] in subfixs:  # 后缀名判断
                    imglist.append(filePath)
                else:
                    continue

        # print(imglist)
        retlist = []
        for imgpath in imglist:
            ret = self.recognize(imgpath)
            retlist.append((ret[0], ret[1], imgpath))

        print(retlist)
        return retlist

    def recognize(self, imgpath):
        img = Image.open(imgpath)
        if not img:
            print("不能识别", imgpath)
            return

        print("=======开始识别=======", imgpath)
        s = pytesseract.image_to_string(img, lang="chi_sim+eng")
        s = s.replace(" ", "").replace("\n","").replace("\r","")

        # print(pytesseract.get_languages(config=""))
        # s = pytesseract.image_to_data(img, lang="chi_sim")
        print(s)

        # 识别健康码, 查找时间戳 如 20:27:13
        if "浙江健康码" in s:
            idx = s.index("浙江健康码")
            if idx:
                print("识别到<健康码>")
                time = re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", s)
                if time:
                    flag1 = s.find(time[0])
                    #取姓名长度
                    namelen = 4
                    name = s[flag1+8: flag1+8+namelen]
                    print('匹配姓名：',name)
                    return (CardType.HealthCard, name)

            # flag2 = s.index("代办")

        # 识别行程码
        idx = -1
        idx = s.find("的动态行程卡")
        if idx:
            print("识别到<行程卡>")
            pp = re.findall("1[0-9]{2}[*|x|X]*[0-9]{4}", s)
            if pp:
                pn = pp[0]
                pn = pn[0:3] + "****" + pn[len(pn)-4:len(pn)]
                print('匹配手机号：',pp)
                return (CardType.TravalCard, pn)

        return (CardType.UnknownCard, "")

ocr = HeathCodeRecognition(os.getcwd() + "/images")
ocr.findFile()