'''
生成01矩阵
'''
import cv2
import numpy as np
def pengzhang(corrected):
    height, width, _ = corrected.shape
    height7 = height
    width7 = width
    gray = cv2.cvtColor(corrected, cv2.COLOR_BGR2GRAY)
    global treasures
    treasures = []
    # 找到宝藏点坐标
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=15, minRadius=5, maxRadius=15)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            treasures.append((x, y))

    # print(treasures)
    # 自适应阈值

    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 2)
    kernel = np.ones((4, 4), np.uint8)

    dilated = cv2.dilate(thresh2, kernel, iterations=1)
    # 腐蚀操作
    eroded = cv2.erode(dilated, kernel, iterations=8)
    height, width = eroded.shape
    height5 = height
    width5 = width
    # 保留矩形内部的内容 切割图片
    found = False
    for n in range(20):
        for m in range(20):
            for j in range(20):
                for i in range(20):
                    if (np.mean(eroded[i:i + 1, n:width5 - m]) == 0 and
                            np.mean(eroded[height5 - j - 1:height5 - j, n:width5 - m]) == 0
                            and np.mean(eroded[i:height, width - m - 1:width - m]) == 0):
                        roi = eroded[i:height - j, n:width - m]
                        rowi = i
                        colj = j
                        colm = m
                        rown = n
                        print(rowi, colj, colm, rown)
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
            # 宝藏点的坐标转换
    roi = eroded[i:height - j, n:width - m]
    rowi = i
    colj = j
    colm = m
    rown = n
    for i in range(len(treasures)):
        x, y = treasures[i]
        x_transformed = round_to_nearest((x - colm - rown) / (height7 - colm - rown) * 21)
        y_transformed = round_to_nearest((y - rowi - colj) / width7 * 21)
        treasures[i] = (x_transformed, y_transformed)
    # print(treasures)
    # 对切割得到的图片进行格式重处理
    eroded2 = cv2.resize(roi, (525, 525))
    return eroded2


def gezi(eroded2):
    # 计算单元格大小
    height, width = eroded2.shape[:2]
    cell_size = min(height, width) // 21
    # 初始化迷宫数组
    maze = np.ones((21, 21), dtype=int)
    # 遍历每个单元格
    for i in range(21):
        for j in range(21):
            # 计算单元格的位置和大小
            x = j * cell_size
            y = i * cell_size
            w = cell_size
            h = cell_size
            # 计算单元格的灰度均值

            # 中心x，y
            centerx = int(x + w / 2)
            centery = int(y + h / 2)
            # 切片单元格中心9格像素的区域
            cell = eroded2[centery:centery + 3, centerx:centerx + 3]
            mean = np.mean(cell)
            # 判断单元格是否为墙
            if mean > 0:
                maze[i, j] = 0
                cv2.rectangle(eroded2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.rectangle(eroded2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("chuli", eroded2)
    cv2.imwrite("chuli.jpg", eroded2)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    # print(maze)
    return maze


def round_to_nearest(num):
    if num - int(num) >= 0.5:
        return int(num) + 1
    else:
        return int(num)


def modify_maze(maze, treasures):
    import coordinate_call  #
    treasures = coordinate_call.mixed_rows(coordinate_call.coordinate_call())  #
    for treasure in treasures:
        treasure_x, treasure_y = treasure
        maze[treasure_y][treasure_x] = 0
    return maze