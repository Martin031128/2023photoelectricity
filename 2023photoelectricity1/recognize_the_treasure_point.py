
'''
识别宝藏点
'''
# -*- codeing = utf-8 -*-
# @Time : 2022/3/23 17:13

import math
import csv
import os
import cv2
import numpy as np
import socket

def is_duplicate(new_x, new_y):
    with open("test1.csv", "r", encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # 跳过表头
        try:
            header = next(reader)
        except StopIteration:
            # CSV文件为空
            return False
        for row in reader:
            if not row:
                continue
            old_x, old_y = row
            if abs(float(old_x) - new_x) <= 1 and abs(float(old_y) - new_y) <= 3:  # 在范围内变化的值不会被写入
                print(old_x)
                print(new_x)
                return True
    return False


def file_deal(file_name):
    try:
        file_name = 'test1.csv'
        files = open(file_name, "rb")
        mes = files.read()
    # print(mes)
    # print(type(mes))
    except:
        print("没有该文件")
    else:
        files.close()
    return mes


def mwin():
    # while True:
    mes = file_deal('test1.csv')


#     mes=list


def cvt_pos(pos, cvt_mat_t):
    u = pos[0]
    v = pos[1]
    x1 = (cvt_mat_t[0][0] * u + cvt_mat_t[0][1] * v + cvt_mat_t[0][2]) / (
                cvt_mat_t[2][0] * u + cvt_mat_t[2][1] * v + cvt_mat_t[2][2])
    y1 = (cvt_mat_t[1][0] * u + cvt_mat_t[1][1] * v + cvt_mat_t[1][2]) / (
                cvt_mat_t[2][0] * u + cvt_mat_t[2][1] * v + cvt_mat_t[2][2])
    return (x1, y1)


def circle(img):
    a = []
    b = []
    # image = cv2.imread(img)
    h, w, c = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=200, param2=15, minRadius=8, maxRadius=15)
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=15, minRadius=5, maxRadius=15)
    # print("circlesshi",circles)
    # if circles[0,0,0]!=None:

    if circles is not None:
        for i in circles[0, :]:

            # print(type((i[0], i[1])))
            cv2.circle(img, (int(i[0]), int(i[1])), int(i[2]), (0, 0, 255), 2)  # 画圆

            # print(i[0],i[1])
            a.append(i[0])
            b.append(i[1])

            x1, y1 = i[0], i[1]
            print('宝藏像素坐标为：', a[len(a) - 1], b[len(b) - 1])

            list = [x1, y1]
            file_exists = False
            try:
                # 检查CSV文件是否存在
                with open("test1.csv", "r", encoding='utf-8') as checkfile:
                    check_reader = csv.reader(checkfile)
                    # 检查CSV文件是否为空
                    if not any(check_reader):
                        # 文件为空，写入表头行
                        with open("test1.csv", mode='w', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            # writer.writerow(["X-coordinate", "Y-coordinate"])
                    file_exists = True
            except FileNotFoundError:
                # 文件不存在，稍后将创建
                pass
            if not is_duplicate(math.floor(x1 / (h / 21)), math.floor(y1 / (h / 21))):
                # 将新行数据追加到CSV文件末尾
                with open("test1.csv", mode='a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    # 如果文件不存在，写入表头行
                    if not file_exists:
                        writer.writerow(["X-coordinate", "Y-coordinate"])
                    writer.writerow([math.floor(x1 / (h / 21)), math.floor(y1 / (h / 21))])