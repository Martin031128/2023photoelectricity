import cv2
import numpy as np
import time
'''
识别定位点
'''
import recognize_the_anchor_point
coordinates=recognize_the_anchor_point.recognize_the_anchor_point()

import filter_coordinate

threshold = 20
filtered_coords = filter_coordinate.remove_similar_coordinates(coordinates, threshold)
print("The filtered coordinates: ", filtered_coords)
# 获取重复次数最多的四个坐标
filtered_coords = filter_coordinate.find_most_frequent_coordinates(coordinates)
print("filtered_coords: ", filtered_coords)

# 计算坐标和，找出最大和最小坐标
sum_coordinates = [sum(coord) for coord in filtered_coords]
max_coord = filtered_coords[sum_coordinates.index(max(sum_coordinates))]
min_coord = filtered_coords[sum_coordinates.index(min(sum_coordinates))]

# 删除最大和最小坐标，并按x的大小降序排序
sorted_coords = sorted([coord for coord in filtered_coords if coord != max_coord and coord != min_coord],
                       key=lambda x: x[0], reverse=True)

# 添加最大和最小坐标到重新排序的数组中
filtered_coords = [max_coord] + sorted_coords + [min_coord]


# 打印结果
print(f"after adjustment: ", filtered_coords)
'''
识别宝藏点
'''
import perspective_transformation
perspective_transformation.perspective_transformation(filtered_coords)