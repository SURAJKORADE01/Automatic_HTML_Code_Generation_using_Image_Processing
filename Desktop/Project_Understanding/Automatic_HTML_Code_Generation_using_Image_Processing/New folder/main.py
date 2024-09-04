# importing modules
from ensurepip import bootstrap
import cv2
import pytesseract
import csv
import numpy as np
# reading image using opencv
import stackpath as stackpath
from pandas.io.formats import css
from pytesseract import Output
from imutils import grab_contours as grb_cns
from imutils import resize as rsz
from keras.models import load_model
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\Tesseract.exe'
approx = load_model('trModel.h5')
# importing modules
from ensurepip import bootstrap

image = cv2.imread('sample.png')
output = image.copy()
# converting image into gray scale image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

of = open("sample.html", "w")
#html = "<html><head><link rel = 'stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css' integrity='sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB' crossorigin='anonymous'><style>.box{border:1px solid black;} </style></head><body>"

html = "<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6' crossorigin='anonymous'><style>.box{border:1px solid black;} </style></head><body>"

(_, threshold) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
(contours, _) = cv2.findContours(threshold, cv2.RETR_TREE,
                                 cv2.CHAIN_APPROX_SIMPLE)
#cns = grb_cns(contours)
# converting it to binary image by Thresholding
# this step is require if you have colored image because if you skip this part
# then tesseract won't able to detect text correctly and this will give incorrect result
threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# display image
cv2.imshow('threshold image', threshold_img)
# Maintain output window until user presses a key
cv2.waitKey(0)
# Destroying present windows on screen
cv2.destroyAllWindows()

# configuring parameters for tesseract
custom_config = r'--oem 3 --psm 6'
# now feeding image to tesseract
details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')
print(details)

total_boxes = len(details['text'])
for sequence_number in range(total_boxes):
    if int(details['conf'][sequence_number]) > 40:
        (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],details['height'][sequence_number])
        div = "<span style='"
        div = div + "position: absolute;"
        div = div + "left: " + str(x) + ";"
        div = div + "top: " + str(y) + ";"
        div = div + "width: " + str(w) + ";"
        div = div + "height: " + str(h) + ";"
        div = div + "'>" + details["text"][sequence_number]
        div = div + "</span>"
        html = html + "\n" + div
        threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# display image
cv2.imshow('captured text', threshold_img)

# Maintain output window until user presses a key

cv2.waitKey(0)
# Destroying present windows on screen

cv2.destroyAllWindows()

parse_text = []
word_list = []
last_word = ''
for word in details['text']:
    if word != '':
        word_list.append(word)
        last_word = word
    if (last_word != '' and word == '') or (word == details['text'][-1]):
        parse_text.append(word_list)
        word_list = []

for cnt in contours:
    area = cv2.contourArea(cnt)
    p = cv2.arcLength(cnt,True)

    if area > 400:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt,
                                                             True), True)
    if len(approx) == 4:
        cv2.drawContours(image, [approx], 0, (0, 0, 0xFF), 5)
        x, y, w, h = cv2.boundingRect(cnt)
        print("approx ", x, y, w, h)

#for text box
        if w > 50 and w<500:
            div = "<div class='box' style='"
            div = div + "position: absolute;"
            div = div + "left: " + str(x) + ";"
            div = div + "top: " + str(y) + ";"
            div = div + "width: " + str(w) + ";"
            div = div + "height: " + str(h) + ";"
            div = div + "'><input type='text' /></div>"
            html = html + "\n" + div

        elif w < 40 and h > 30:
            div = "<div class='check_box' style='"
            div = div + "position: absolute;"
            div = div + "left: " + str(x) + ";"
            div = div + "top: " + str(y) + ";"
            div = div + "width: " + str(w) + ";"
            div = div + "height: " + str(h) + ";"
            div = div + "'><input type='checkbox' /></div>"
            html = html + "\n" + div

#for radio button

    elif len(approx) == 8 and int(p) == 64:

        cv2.drawContours(image, [cnt], -1, (180, 105, 255), 3)
        x, y, w, h = cv2.boundingRect(cnt)
        print("approx ", x, y, w, h)
        if w<10 and h<10:
            div = "<div class='radio_button' style='"
            div = div + "position: absolute;"
            div = div + "left: " + str(x) + ";"
            div = div + "top: " + str(y) + ";"
            div = div + "width: " + str(w) + ";"
            div = div + "height: " + str(h) + ";"
            div = div + "'><input type='radio' /></div>"
            html = html + "\n" + div

#for checkbox

    elif len(approx) == 4 and int(p) == 73:
            cv2.drawContours(image, [cnt], -1, (180, 105, 255), 3)
            x, y, w, h = cv2.boundingRect(cnt)
            print("approx ", x, y, w, h)
            if w < 40 and h > 30:
                div = "<div class='check_box' style='"
                div = div + "position: absolute;"
                div = div + "left: " + str(x) + ";"
                div = div + "top: " + str(y) + ";"
                div = div + "width: " + str(w) + ";"
                div = div + "height: " + str(h) + ";"
                div = div + "'><input type='checkbox' /></div>"
                html = html + "\n" + div

html = html + '</body></html>'

of.write(html)
of.close()

with open('result.txt', 'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(parse_text)

if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()