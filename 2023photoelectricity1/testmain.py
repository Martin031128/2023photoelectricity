import cv2
import numpy as np
import time
'''
识别定位点
'''
import recognize_the_anchor_point
coordinates=recognize_the_anchor_point.recognize_the_anchor_point()

'''
提出正确定位点
'''

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

'''
提出起点终点坐标（根据需要使用）
'''
import extract_the_blue_and_red_coordinate
extract_the_blue_and_red_coordinate.extract_the_blue_and_red_coordinate("corp_rotated.jpg")

'''
去除红蓝色
'''
import remove_the_blue_and_red
remove_the_blue_and_red.remove_the_blue_and_red("corp_rotated.jpg")

'''
生成01矩阵
'''
import generate_the_01_matriix
imgs = cv2.imread("Result.jpg")

# 主函数
# 迷宫地图
import coordinate_call

a = coordinate_call.mixed_rows(coordinate_call.coordinate_call())
treasures = a
eroded2 = generate_the_01_matriix.pengzhang(imgs)
maze = generate_the_01_matriix.gezi(eroded2)
maze = generate_the_01_matriix.modify_maze(maze, treasures)
print(maze)

'''
路径规划
'''

import route_planning

a = coordinate_call.mixed_rows(coordinate_call.coordinate_call())
treasures_before = a
maze = np.array(maze)
print(f"get treasure point from csv: ", a)
# start = (math.ceil((x+x+w)/2/34), math.floor((y+y+h)/2/34))
# end = (math.ceil((x1+x1+w)/2/34), math.floor((y1+y1+w)/2/34))
start = (19, 19)
end = (1, 1)
print("start", start)
print("end", end)

treasures_after = route_planning.get_treasures(maze, treasures_before)
print("treasures_after: ", treasures_after)
treasures_copy = treasures_after[:]
path = route_planning.combine_paths(maze, start, treasures_after, end)
cross_corner = route_planning.judge_cross_corner(maze)
t_corner = route_planning.judge_T_corner(maze)
print(route_planning.get_turn_points_else(maze, path, t_corner, cross_corner, treasures_copy))
arr = route_planning.get_turn_points_else(maze, path, t_corner, cross_corner, treasures_copy)
# output_str = ' '.join(arr)
# print(output_str)

route_planning.drew_shortest_path(maze, start, treasures_copy, end)
cv2.waitKey(1000)
cv2.destroyAllWindows()

'''
发送命令给nano
'''
# send to stm32
import serial

print(arr)
output_str = ' '.join(arr)
output_str_f = "'{}'".format(output_str)
print(output_str_f)
ser = serial.Serial('/dev/ttyACM0', 115200)
data = bytes.fromhex(output_str)
print(data)
ser.write(data)
ser.close()

