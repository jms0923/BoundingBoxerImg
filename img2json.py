import os
import copy
import cv2
from collections import OrderedDict
import json
import gt2coco
from tqdm import tqdm

# allCategoryList = ['bottle', 'plastic']
# allCategoryList = list(gt2coco.labelIdx.keys())

path = "./"
allgttxt = []
fileNumber = {}
idUniq = 1

def imgID(fileList):
    global fileNumber
    for idx, file in enumerate(iterable=fileList, start=1):
        toJpg = file.split(".")[0]
        fileNumber[toJpg] = idx


# get gt txt list
def getfilelist(pathDir):
    filelist = os.listdir(pathDir)
    file_list_txt = [file for file in filelist]
    return file_list_txt


#read_gt_file
def readgtfile(pathdir, filename):
    f = open(pathdir + filename, 'r')
    while True:
        line = f.readline()
        if not line: break
        allgttxt.append(line)
    f.close()

    return allgttxt


#split allgttxt
def splitgttxt(allgttxt):
    splitlist = allgttxt.split(",")

    return splitlist


# make info
def makeInfo():
    info = OrderedDict()
    info["description"] = "DSL"
    info["url"] = "https://supercom.korea.ac.kr/"
    info["version"] = "0.1"
    info["date_created"] = "2020/07/07"

    return info


# make images
# full screen image 
def makeImages(pathDir):
    print('make images annotations ...')

    global idUniq
    allFileList = os.listdir(pathDir)
    imgExt = ['.jpg', '.jpeg', '.JPG', '.JPEG']
    fileList = [f for f in allFileList if f.endswith(tuple(imgExt))]
    images = []
    licenses = OrderedDict()
    for i in tqdm(fileList):
        if i.split('.')[-1] is not 'json':
            imgShape = cv2.imread(os.path.join(pathDir, i)).shape
            licenses["license"] = 1
            licenses["file_name"] = i
            licenses["coco_url"] = "None"
            licenses["height"] = imgShape[0]
            licenses["width"] = imgShape[1]
            licenses["date_captured"] = "2020-03-10 15:00:00"
            licenses["flickr_rul"] = "None"
            licenses["id"] = idUniq
            idUniq += 1
            images.append(copy.deepcopy(licenses))
            licenses.clear()

    return images


def makeLicenses():
    licenseList = []
    licenseButton = OrderedDict()
    licenseButton["url"] = "https://supercom.korea.ac.kr/"
    licenseButton["id"] = 1
    licenseButton["name"] = "Attribution-NonCommercial License"
    licenseList.append(licenseButton)

    return licenseList


# make categories
def makeCategories():
    categoryList = []
    category = OrderedDict()
    idNum = 1

    # do not change order
    # supercatetory text
    # supercatetory Switch
    allCategoryList = list(gt2coco.labelIdx.keys())

    for name in allCategoryList:
        category["supercategory"] = name
        category["id"] = idNum
        idNum += 1
        category["name"] = name
        categoryList.append(copy.deepcopy(category))
        category.clear()

    return categoryList


def jsonSave(jsonObj, fileName):
    with open(fileName, 'w', encoding='utf-8') as make_file:    # "./" +
        json.dump(jsonObj, make_file, indent="\t")


def writeJson(jsonObj, dir, fileName):
    jsonObj["categories"] = makeCategories()
    jsonSave(jsonObj, os.path.join(dir, fileName))
    print('\n----------write json file----------\n')


# make one annotation
def makeAnnotation(allgttxt, number, annotationsID):
    annotation = OrderedDict()
    splitgttxt = allgttxt.split(",")

    x = int(splitgttxt[0]) 
    y = int(splitgttxt[1])
    w = int(splitgttxt[2]) - int(splitgttxt[0]) # x
    h = int(splitgttxt[5]) - int(splitgttxt[1]) # y

    segeList = [[x, y, x+w, y, x+w, y+h, x, y+h]]
    catrgoryName = splitgttxt[-1].split("\n")[0][0]
    categoryID = gt2coco.labelIdx[catrgoryName]
    print(catrgoryName, categoryID)
    # if catrgoryName == 'bottle':
    #     categoryID = 1
    # # elif catrgoryName == 'can':
    # #     categoryID = 2
    # # elif catrgoryName == 'general':
    # #     categoryID = 3
    # # elif catrgoryName == 'iron':
    # #     categoryID = 3
    # # elif catrgoryName == 'paper':
    # #     categoryID = 4
    # elif catrgoryName == 'plastic':
    #     categoryID = 2
    # # elif catrgoryName == 'strofoam':
    # #     categoryID = 6
    # # elif catrgoryName == 'vinyl':
    # #     categoryID = 7

    annotation["segmentation"] = segeList
    annotation["area"] = w * h
    annotation["iscrowd"] = 0
    annotation["image_id"] = int(number)
    annotation["bbox"] = [x, y, w, h]
    annotation["category_id"] = categoryID
    annotation["id"] = annotationsID

    return annotation


def main(txtdir, imgdir, jsonDir, annoName):

    jsonWhole = OrderedDict()
    annotations = []
    count = 0
    annotationsID = 1
    jsonFileName = annoName + ".json"
    # jsonDir = "./annotations/"

    filelist = getfilelist(txtdir)    # txt file read
    imgID(filelist)

    jsonWhole["info"] = makeInfo()
    jsonWhole["licenses"] = makeLicenses()
    print("make images ...")
    jsonWhole["images"] = makeImages(imgdir)
    jsonWhole["categories"] = makeCategories()

    #json
    print("write json about images")
    writeJson(jsonWhole, jsonDir, jsonFileName)






if __name__ == '__main__':

    serverSourceDir = "./jinOut/txt/"
    serverResultDir = "./jinOut/jpg/"
    localSourceDir = "./jinOut/"
    localResultDir = "instances_train2017"

    labelPath = "./jinOut/labels/"
    jsonPath = "./jinOut/" + localResultDir + ".json"


    main(serverSourceDir, serverResultDir, localSourceDir, localResultDir)
