'''
去除红蓝色
'''
def remove_the_blue_and_red(imgs_path):
    import cv2
    import glob
    import numpy as np
    import queue
    import heapq

    imgs = cv2.imread(imgs_path)
    #####
    hsv_image = cv2.cvtColor(imgs, cv2.COLOR_BGR2HSV)

    # 定义红色和蓝色的阈值范围
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    upper_red2 = np.array([220, 255, 255])
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([150, 255, 255])

    # 创建红色和蓝色的掩码
    red_mask1 = cv2.inRange(hsv_image, lower_red, upper_red)
    red_mask2 = cv2.inRange(hsv_image, lower_red, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # 合并红色和蓝色的掩码
    merged_mask = cv2.bitwise_or(red_mask, blue_mask)

    # 将掩码应用于图像
    target_color = (255, 255, 255)
    result = imgs.copy()
    result[np.where(merged_mask > 0)] = target_color
    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # # 设定阈值

    # 待改
    threshold = 80

    # # # 使用阈值化将灰色像素提取出来
    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    # # 将灰色像素替换为白色像素
    output_image = cv2.bitwise_or(binary_image, gray_image)
    # 待改
    kernel = np.ones((3, 3), np.uint8)

    # 腐蚀操作
    eroded = cv2.erode(output_image, kernel, iterations=4)

    # 膨胀操作
    dilated = cv2.dilate(eroded, kernel, iterations=1)
    # 显示原始图像和处理后的图像
    # cv2.imshow('Original Image', imgs)
    # cv2.imshow('out',output_image)
    cv2.imshow('Result', dilated)
    cv2.imwrite('Result.jpg', dilated)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    