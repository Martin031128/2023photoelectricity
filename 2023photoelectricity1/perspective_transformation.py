def perspective_transformation(filtered_coords):
    import recognize_the_treasure_point
    import cv2
    import numpy as np
    import time
    import csv
    file_path = "/home/buwai/yolov5-seg/test1.csv"

    # 使用 open 函数打开文件并清空内容
    with open(file_path, "w") as file:
        pass  # 什么都不做

    vc = cv2.VideoCapture(0)  # 使用外接摄像头还是内置摄像头
    c = 1
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
    timeF = 1  # 视频帧计数间隔频率

    import time  # 计时程序

    start_time = time.time()
    while True:  # 循环读取视频帧
        rval, frame = vc.read()
        if (c % timeF == 0):  # 每隔timeF帧进行存储操作

            pts1 = np.float32(filtered_coords)
            # pts2 = np.float32([[720, 720], [720, 0], [0, 720], [0, 0]])
            pts2 = np.float32([[0, 0], [0, 720], [720, 0], [720, 720]])
            # 生成透视变换矩阵；进行透视变换
            M = cv2.getPerspectiveTransform(pts1, pts2)

            dst = cv2.warpPerspective(frame, M, (720, 720))
            cv2.imwrite('dst_before.jpg', dst)
            # print("w is:", w)
            # print("h is: ", h)
            alpha = 1.2
            xx = int(alpha * 60)
            yy = int(alpha * 60)
            width = int(720 - alpha * 120)
            height = int(720 - alpha * 120)
            corp_image = dst[yy:yy + height, xx:xx + width]
            # cv2.imshow('dst2',corp_image)

            cv2.imwrite('circles.jpg', corp_image)
            cv2.waitKey(0)
            # cv2.imshow('imgshow', dst)  # xianshi为图像

            (h, w) = dst.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, 180, 1.)  # 顺时针旋转
            rotated = cv2.warpAffine(corp_image, M, (w, h))

            xx = 720 - width
            yy = 720 - height
            corp_rotated = rotated[yy:yy + height, xx:xx + width]
            cv2.imshow('corp_rotated', corp_rotated)
            cv2.imwrite('corp_rotated.jpg', corp_rotated)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
            recognize_the_treasure_point.circle(corp_rotated)

        cv2.waitKey(1)
        if time.time() - start_time >= 5:  # 拍摄十秒钟后停止
            break