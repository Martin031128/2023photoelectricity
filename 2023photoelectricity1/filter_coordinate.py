
'''
提出定位点
'''
import math


def distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def remove_similar_coordinates(coords, threshold):
    result = []
    for i in range(len(coords)):
        is_unique = True
        for j in range(i + 1, len(coords)):
            if distance(coords[i], coords[j]) <= threshold:
                is_unique = False
                break
            if is_unique:
                result.append(coords[i])
    return result


# threshold = 20
# filtered_coords = remove_similar_coordinates(coordinates, threshold)
# print("The filtered coordinates: ", filtered_coords)

from collections import Counter


def find_most_frequent_coordinates(coordinates):
    # 统计坐标的出现次数
    counts = Counter(coordinates)

    # 按照次数进行排序
    sorted_coordinates = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # 取出前四个重复次数最多的坐标
    top_four = [coord for coord, count in sorted_coordinates[:4]]

    return top_four


# # 获取重复次数最多的四个坐标
# filtered_coords = find_most_frequent_coordinates(coordinates)
# print("filtered_coords: ", filtered_coords)
#
# # 计算坐标和，找出最大和最小坐标
# sum_coordinates = [sum(coord) for coord in filtered_coords]
# max_coord = filtered_coords[sum_coordinates.index(max(sum_coordinates))]
# min_coord = filtered_coords[sum_coordinates.index(min(sum_coordinates))]
#
# # 删除最大和最小坐标，并按x的大小降序排序
# sorted_coords = sorted([coord for coord in filtered_coords if coord != max_coord and coord != min_coord],
#                        key=lambda x: x[0], reverse=True)
#
# # 添加最大和最小坐标到重新排序的数组中
# filtered_coords = [max_coord] + sorted_coords + [min_coord]
#
# # 打印结果
# print(f"after adjustment: ", filtered_coords)
