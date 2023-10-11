'''
提出起点终点坐标（根据需要使用）
'''
def extract_the_blue_and_red_coordinate(image_path):

    import cv2
    import numpy as np

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    blue_lower = np.array([100, 90, 90])
    blue_upper = np.array([150, 255, 255])

    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)

    # image[red_mask > 0] = [255, 255, 255]         #将红蓝变成白色
    # image[blue_mask > 0] = [255, 255, 255]

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours = [cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True) for cnt in contours]

    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours = [cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True) for cnt in contours]

    for red_contour in red_contours:
        (x, y, w, h) = cv2.boundingRect(red_contour)
        print("Red Square: Top left: ({}, {}), Bottom right: ({}, {})".format(x, y, x + w, y + h))

    for blue_contour in blue_contours:
        (x1, y1, w1, h1) = cv2.boundingRect(blue_contour)
        print("Blue Square: Top left: ({}, {}), Bottom right: ({}, {})".format(x1, y1, x1 + w1, y1 + h1))

    # 保存处理后的图片
    cv2.imwrite("processed_image.jpg", image)
    return image

