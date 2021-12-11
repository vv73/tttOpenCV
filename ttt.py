import os
import shutil
import sys
import time


import numpy as np
from cv2 import cv2


X = "X"
O = "O"

def mouse_drawing(event, x, y, flags, params):
    global gl_point1, gl_point2, selecting

    if event == cv2.EVENT_LBUTTONDOWN:
        selecting = True
        gl_point1 = (x, y)
        gl_point2 = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if selecting is True:
            gl_point2 = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        selecting = False
        print('finished square')
    elif event == cv2.EVENT_RBUTTONUP:
        selecting = False
        gl_point1 = gl_point2 = None

cap = cv2.VideoCapture("rtsp://admin:12345678@192.168.100.159:10554/tcp/av0_0")
# cap = cv2.VideoCapture("rtsp://admin:12345678@10.8.134.131:10554/tcp/av0_0")
# cap = cv2.VideoCapture(0)

WINDOW_TITLE = "Tic-Tac-Toe OpenCV"
frame = cv2.namedWindow(WINDOW_TITLE)
thr = cv2.namedWindow("Thresh")
def threshold(_):
    pass
cv2.createTrackbar('Threshold', "Thresh", 130, 255,  threshold)

def detect_board(contours, hierarchy):
    for i, c in enumerate(contours):
        if cv2.arcLength(c, True) < 50:
            continue
        epsilon = 0.02 * cv2.arcLength(c, True)
        poly = cv2.approxPolyDP(c, epsilon, True)
        if len(poly) == 20:
            if hierarchy[0][i][2] != -1:
                inside = contours[hierarchy[0][i][2]]
                epsilon = 0.02 * cv2.arcLength(inside, True)
                poly = cv2.approxPolyDP(inside, epsilon, True)
                if len(poly) == 4:
                    return i
    return None

def dist2(p1, p2):
    # print(p1, p2)
    d = (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])
    return d


def detect_sign(contour):
    '''NOUGHT or CROSS'''
    center, r = cv2.minEnclosingCircle(contour)
    mind = r * r
    for p in contour:
        d = dist2(p[0], center)
        if d < mind:
            mind = d
    # print(mind / (r * r))
    if mind / (r * r) < 0.1:
        return X
    else:
        return O
    print("bad", mind / (r * r))
    return None

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    cv2.imshow(WINDOW_TITLE, frame)
    # Переводим изображение в монохром
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (3,3))
    # Забираем и используем значение с trackbar'a
    _, trFrame = cv2.threshold(gray, cv2.getTrackbarPos('Threshold', "Thresh"), 255, cv2.THRESH_BINARY_INV)

    cnts, hierarchy = cv2.findContours(trFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boardInd = detect_board(cnts, hierarchy)
    cv2.drawContours(frame, cnts, boardInd, (255, 255, 0), 3)
    for i, c in enumerate(cnts):
        if i == boardInd:
            continue
        if cv2.arcLength(c, True) < 50:
            continue
        if detect_sign(c) == X:
            cv2.drawContours(frame, cnts, i, (255, 0, 0), 2)
        else:
            cv2.drawContours(frame, cnts, i, (0, 0, 255), 2)

    cv2.imshow(WINDOW_TITLE, frame)
    cv2.imshow('Thresh', trFrame)
    if cv2.waitKey(1) & 0xFF == 27 or not ret:
        break

cv2.destroyAllWindows()
