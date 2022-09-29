import pytesseract
import os
import glob
import numpy as np
import cv2 as cv
from os import listdir
from os.path import isfile, join
from pdf2image import convert_from_path


PDF_FOLDER_PATH = 'pdfs'
TXT_OUTPUT_PATH = 'txts'


def resize_img(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    return resized


def pdf_to_img(path: str):
    imgs = []
    pages = convert_from_path(path, 500)
    for raw_img in pages:
        numpy_img = np.array(raw_img)
        gray = cv.cvtColor(numpy_img, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        thresh = cv.adaptiveThreshold(
            blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10
        )
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        imagem = cv.bitwise_not(closing)
        imgs.append(imagem)
    return imgs


def img_to_txt_from_file(path: str):
    imgs = glob.glob(path)
    for img_path in imgs:
        img = cv.imread(img_path)
        text = pytesseract.image_to_string(img, lang="pol+equ", config='--psm 1')
    return text


def img_to_txt(img, path, name):
    text = pytesseract.image_to_string(img, lang="pol", config='--psm 6')
    text = text.replace('\n', ' ').strip()

    # print(text)
    # cv.imshow("cnrs.png", img)
    # cv.waitKey(0)

    if len(text) > 5:
        with open(f'{path}/{name}.txt', "a") as f:
            f.write(text)
            f.write("\n")
    return text


def get_boxes_with_content(img):
    contours, _ = cv.findContours(
        img.astype(np.uint8), cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE
    )
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
    rule_box_size = cv.contourArea(sorted_contours[10])
    rule_box_cntrs = [
        cntr
        for cntr in contours
        if 0.3*rule_box_size < cv.contourArea(cntr) < 3*rule_box_size
    ]
    approxed = list(map(get_approx_cntr, rule_box_cntrs))

    # check = cv.cvtColor(img.copy(), cv.COLOR_GRAY2RGB)
    # cv.drawContours(check, approxed, -1, (0,0,255),  5)
    # scaled = resize_img(check, 10)
    # cv.imshow("cnrs.png", scaled)
    # cv.waitKey(0)

    rgb = cv.cvtColor(img.copy(), cv.COLOR_GRAY2RGB)
    cv.drawContours(rgb, approxed, -1, (255,255,255), 7)
    cv.drawContours(rgb, sorted_contours, 1, (255,255,255), 10)

    reshaped = [box.reshape((-1,2)) for box in approxed]
    reshaped = np.flip(reshaped, axis=0)
    return reshaped, rgb

def get_approx_cntr(cnt):
    epsilon = 0.01*cv.arcLength(cnt,True)
    approx = cv.approxPolyDP(cnt,epsilon,True)
    return approx


def crop_img_to_one_question(bounding_boxes, img):
    question_images = []
    for box in bounding_boxes:
        min_x, max_x, _, _ = cv.minMaxLoc(box[:,0])
        min_y, max_y, _, _ = cv.minMaxLoc(box[:,1])
        croped = img[int(min_y):int(max_y), int(min_x+10):int(max_x-10)]
        question_images.append(croped)
        # cv.imshow("croped", croped)
        # cv.waitKey(0)
    return question_images


def get_txts(year):
    try:
        os.remove(f'{TXT_OUTPUT_PATH}/{year}.txt')
    except:
        pass
    pages = pdf_to_img(f'{PDF_FOLDER_PATH}/{year}.pdf')
    for page in pages:
        bounding_boxes, text_img = get_boxes_with_content(page)
        question_images = crop_img_to_one_question(bounding_boxes, text_img)
        for img in question_images:
            img_to_txt(img, TXT_OUTPUT_PATH, year)




if __name__ == '__main__':
    years = [f[:-4] for f in listdir(PDF_FOLDER_PATH) if isfile(join(PDF_FOLDER_PATH, f))]
    for year in years:
        get_txts(year)

    # year = '2009'
    # pages = pdf_to_img(f'pdfs/{year}.pdf')
    # bounding_boxes, rgb = get_boxes_with_content(pages[0])
    # question_images = crop_img_to_one_question(bounding_boxes, rgb)
    # for img in question_images:
    #     img_to_txt(img,TXT_OUTPUT_PATH, year)

    # txt = img_to_txt_from_file('Screenshot from 2022-09-29 22-02-40.png')
    # print(txt)