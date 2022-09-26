import pytesseract
import os
import glob
import numpy as np
import cv2 as cv
from pdf2image import convert_from_path




def resize_img(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    return resized


def pdf_to_img(path: str):
    pdfs = glob.glob(path)

    for pdf_path in pdfs:
        pages = convert_from_path(pdf_path, 500)

        for pageNum,imgBlob in enumerate(pages):
            numpy_img = np.array(imgBlob)
            gray = cv.cvtColor(numpy_img, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray,(5,5),0)
            _, thresh = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

            cv.imwrite(f"{pdf_path[:-4]}_{pageNum}.png", thresh)


def img_to_txt(path: str):
    imgs = glob.glob(path)
    for img_path in imgs:
        img = cv.imread(img_path)
        text = pytesseract.image_to_string(img, lang='pol+equ')
        with open(f'{img_path[:-6]}.txt', 'a') as f:
            f.write(text)


# pdf_to_img(r"exams_keys/2010/*.pdf")
img_to_txt(r"exams_keys/2010/2010_4_1.png")

