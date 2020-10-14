import os
import json
from collections import OrderedDict
import img2json
import copy
import cv2
from tqdm import tqdm

"""
read gt file and make them to annotation file for large dataset
gt form : left_up_x left_up_y right_up_x right_up_y right_down_x right_down_y left_down_x left_down_y
annotation form : coco
"""

# labelIdx = {'paper': 1, 'paperpack': 2, 'papercup': 3, 'can': 4, 'bottle': 5,
#             'pet': 6, 'plastic': 7, 'vinyl': 8, 'cap': 9, 'label': 10}
labelIdx = {}


def openJson(jsonPath):
    with open(jsonPath) as f:
        jsonFile = json.load(f)

    return jsonFile


def txtRead(txtPath):
    try:
        with open(txtPath) as file:
            while True:
                line = file.readline()
                if line == '':
                    break
                yield line.strip('\n')
    except Exception:
        return False


def fileList(path):
    for path, dir, files in os.walk(path):
        return files


def getLebelIndex(label):
    if label == 'plastic bag':
        label = 'plasticBag'
    if label == 'plastic_bag':
        label = 'plasticBag'
    if label == 'Bottle':
        label = 'bottle'
    if label == 'contatiner':
        label = 'container'
    return labelIdx[label]


def checkRange(splited, imgWh):
    for i in range(len(splited)-1):
        coor = int(splited[i])

        if coor < 0:
            print('0 case : ', splited, imgWh)
            splited[i] = 0

        if i == 2:
            if coor > imgWh[0]:
                print('x case : ', splited, splited[4], imgWh)
                splited[2] = imgWh[0]
                splited[4] = imgWh[0]

        elif i == 5:
            if coor > imgWh[1]:
                print('y case : ', splited, splited[5], imgWh)
                splited[5] = imgWh[1]
                splited[7] = imgWh[1]

    return splited

# split allgttxt
def splitgttxt(allgttxt):
    splitlist = allgttxt.split(",")
    splitlist[-1] = splitlist[-1].split('\n')[0]

    return splitlist

def boxSizeCheck(splited, imgDir, fileName):
    h, w, c = cv2.imread(os.path.join(imgDir, fileName)).shape

    for idx, coor in enumerate(splited):
        if int(coor) < 0:
            splited[idx] = 0
            print('~~~~~~~~~~', fileName)

    if int(splited[2]) > w:
        splited[2] = w
        splited[4] = w
        print('~~~~~~~~~~', fileName, splited[2], w)
    if int(splited[5]) > h:
        splited[5] = h
        splited[7] = h
        print('~~~~~~~~~~', fileName, splited[5], h)

    return splited

def getCxywh(splited, jpgPath, fileName):
    label = getLebelIndex(splited[-1])
    # splited = boxSizeCheck(splited[:-1], jpgPath, fileName)
    w = int(splited[4]) - int(splited[0])
    h = int(splited[5]) - int(splited[1])
    x = int(splited[0])
    y = int(splited[1])

    return [label, x, y, w, h]

# make one annotation
def makeAnnotation(cxywh, imgID, annotationsID):
    annotation = OrderedDict()
    c, x, y, w, h = cxywh[:]
    segeList = [[x, y, x+w, y, x+w, y+h, x, y+h]]

    annotation["segmentation"] = segeList
    annotation["area"] = w * h
    annotation["iscrowd"] = 0
    annotation["image_id"] = imgID
    annotation["bbox"] = cxywh[1:]
    annotation["category_id"] = c
    annotation["id"] = annotationsID

    return annotation


def saveJson(jsonPath, jsonData):
    with open(jsonPath, 'w') as f:
        f.write(json.dumps(jsonData))


def bbox2json(txtPath, jsonPath, jpgPath):
    annoList = []
    jsonOrigin = openJson(jsonPath)
    jsonImg = jsonOrigin["images"]
    annoID = 1
    for image in tqdm(jsonImg):
        fileName = image['file_name']
        txtName = 'gt_'+fileName.split('.')[0] + '.txt'   #  +
        # print(txtName)
        h = image['height']
        w = image['width']
        id = image['id']
        thisTxtPath = os.path.join(txtPath, txtName)
        # lines = txtRead(txtPath + txtName)
        with open(thisTxtPath, "r") as f:
            lines = f.readlines()
        # if lines:
            for line in lines:
                try:
                    splited = splitgttxt(line)
                    splited = checkRange(splited, [w, h])
                    cxywh = getCxywh(splited, jpgPath, fileName)
                    annoList.append(makeAnnotation(cxywh, id, annoID))
                    annoID += 1
                except:
                    print(line, txtName)

    jsonOrigin["annotations"] = annoList
    print("save json")
    saveJson(jsonPath, jsonOrigin)


def cocoExport(baseDir, classList):
    global labelIdx
    labelIdx = dict.fromkeys(classList, 1)

    jpgPath = baseDir
    txtPath = os.path.join(baseDir, 'gt')
    savePath = baseDir + "\\"

    jsonName = 'coco'
    print("convert images to annotation file")
    img2json.main(txtPath, jpgPath, savePath, jsonName)

    jsonPath = savePath + jsonName + ".json"
    print("convert bbox to annotation file")
    bbox2json(txtPath, jsonPath, jpgPath)
    print("end")


if __name__ == '__main__':
    # train
    txtPath = "D:\AIGrandChallenge\\2cha\\2cha_train\padding\save_gt"
    jpgPath = "D:\AIGrandChallenge\\2cha\\2cha_train\padding\save_img"
    savePath = "D:\AIGrandChallenge\\2cha\\2cha_train\padding\\"
    jsonName = "instances_train2017"
    print("convert images to annotation file")
    img2json.main(txtPath, jpgPath, savePath, jsonName)

    jsonPath = savePath + jsonName + ".json"
    print("convert bbox to annotation file")
    bbox2json(txtPath, jsonPath, jpgPath)
    print("end")

    # val
    # txtPath = "./trash/28/val/gt/"
    # jpgPath = "./trash/28/val/img/"
    # savePath = "./trash/28/"
    # jsonName = "instances_val2017"    # "instances_val2017"
    # print("convert images to annotation file")
    # img2json.main(txtPath, jpgPath, savePath, jsonName)
    #
    # jsonPath = savePath + jsonName + ".json"
    # print("convert bbox to annotation file")
    # bbox2json(txtPath, jsonPath)
    # print("end")
