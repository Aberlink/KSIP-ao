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
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    return resized


def pdf_to_img(path: str):
    imgs = []
    pages = convert_from_path(path, 500)
    for page_num, raw_img in enumerate(pages):
        numpy_img = np.array(raw_img)
        gray = cv.cvtColor(numpy_img, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (3, 3), 0)
        thresh = cv.adaptiveThreshold(
            blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10
        )
        kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
        closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        imagem = cv.bitwise_not(closing)
        imgs.append(imagem)
        # cv.imwrite(f"{path[:-4]}_{page_num}.png", imagem)
    return imgs


def img_to_txt_from_file(path: str):
    imgs = glob.glob(path)
    for img_path in imgs:
        img = cv.imread(img_path)
        text = pytesseract.image_to_string(img, lang="pol+equ")
        with open(f"{img_path[:-6]}.txt", "a") as f:
            f.write(text)
    return text


def img_to_txt(img, name):
    text = pytesseract.image_to_string(img, lang="pol+equ")
    if len(text) < 3:
        return None
    text = text.replace('\n', ' ')
    with open(f'exams_keys/{name}/{name}.txt', "a") as f:
        f.write(text)
        f.write("\n")
    return text


def get_boxes_with_content(img):
    contours, _ = cv.findContours(
        img.astype(np.uint8), cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE
    )
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
    rule_box_size = cv.contourArea(sorted_contours[4])
    rule_box_cntrs = [
        cntr
        for cntr in contours
        if 0.5*rule_box_size < cv.contourArea(cntr) < 2*rule_box_size
    ]
    approxed = list(map(get_approx_cntr, rule_box_cntrs))

    # rgb = cv.cvtColor(img.copy(), cv.COLOR_GRAY2RGB)
    # cnrs = cv.drawContours(rgb, approxed, -1, (0,255,0), 2)
    # cv.imwrite("cntrs.png", rgb)

    reshaped = [box.reshape((-1,2)) for box in approxed]
    reshaped = np.flip(reshaped, axis=0)
    return reshaped

def get_approx_cntr(cnt):
    epsilon = 0.01*cv.arcLength(cnt,True)
    approx = cv.approxPolyDP(cnt,epsilon,True)
    return approx


def crop_img_to_one_question(bounding_boxes, img):
    question_images = []
    for box in bounding_boxes:
        min_x, max_x, _, _ = cv.minMaxLoc(box[:,0])
        min_y, max_y, _, _ = cv.minMaxLoc(box[:,1])
        croped = img[int(min_y+10):int(max_y-30), int(min_x+10):int(max_x-10)]
        question_images.append(croped)
    # cv.imwrite("croped.png", question_images[3])
    return question_images


year = '2013'
pages = pdf_to_img(f'exams_keys/{year}/{year}.pdf')
bounding_boxes = get_boxes_with_content(pages[0])
question_images = crop_img_to_one_question(bounding_boxes, pages[0])

try:
    os.remove(f'exams_keys/{year}/{year}.txt')
except:
    pass

for img in question_images:
    img_to_txt(img, year)






# img_to_txt(r"exams_keys/2012/*.png")


# text = img_to_txt("croped.png")
# text = text.replace('\n', ' ')
# text = text + '\n'

# with open(f"xxx.txt", "a") as f:
#     f.write(text)
#     f.write('\n')
