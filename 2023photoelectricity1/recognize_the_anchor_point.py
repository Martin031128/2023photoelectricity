def recognize_the_anchor_point():
    import cv2
    import numpy as np
    import time

    cap = cv2.VideoCapture(0)

    start_time = time.time()
    coordinates = []  # 存储相近坐标的列表

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)

            if w > 30 and w < 140 and w / h > 2 / 3 and w / h < 1.5 and area > 800 and area < 8000:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                moments = cv2.moments(contour)  # 计算轮廓的矩
                # print("moments is :",moments)
                center_x = int(moments["m10"] / moments["m00"])  # 计算x坐标中心
                center_y = int(moments["m01"] / moments["m00"])  # 计算y坐标中心
                center_coordinates = (center_x, center_y)
                print("center_coordinates: ", center_coordinates)

                # 将坐标添加到列表中
                coordinates.append((center_x, center_y))

        cv2.imshow("Frame", frame)
        cv2.imwrite('image.jpg', frame)
        # 检查是否达到了十秒时间限制
        elapsed_time = time.time() - start_time
        if elapsed_time >= 8:
            break

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # 将相近的坐标组成矩阵
    print(coordinates)
    return coordinates