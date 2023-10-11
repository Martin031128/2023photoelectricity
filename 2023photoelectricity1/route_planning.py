'''
路径规划
'''
import matplotlib.pyplot as plt
import math
import coordinate_call
import cv2
import numpy as np

# 获取宝藏点方法
def get_treasures(maze, treasures):
    valid_treasures = []

    for treasure in treasures:
        if (maze[treasure] != 1).any():
            valid_treasures.append(treasure)

    return valid_treasures


def plot_maze(maze):
    # 获取迷宫的行数和列数
    rows, cols = maze.shape

    # 创建一个与迷宫大小相同的图像
    fig, ax = plt.subplots(figsize=(cols, rows))

    # 遍历迷宫的每一个格子
    for i in range(rows):
        for j in range(cols):
            # 如果是可走的格子，用白色表示
            if maze[i][j] == 0:
                ax.add_patch(plt.Rectangle((j, rows - i - 1), 1, 1, facecolor='white'))
            # 如果是墙壁，用黑色表示
            elif maze[i][j] == 1:
                ax.add_patch(plt.Rectangle((j, rows - i - 1), 1, 1, facecolor='black'))
            elif maze[i][j] == 2:
                ax.add_patch(plt.Rectangle((j, rows - i - 1), 1, 1, facecolor='red'))
            elif maze[i][j] == 3:
                ax.add_patch(plt.Rectangle((j, rows - i - 1), 1, 1, facecolor='yellow'))

    # 设置坐标轴范围和刻度
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    # 显示图像
    plt.show()


# Example treasure location
# 使用 BFS 算法求解最短路径，并返回一个表示路径的列表：

def bfs(maze, start, end):
    queue = [start]
    visited = set()
    parent = {}
    visited.add(start)
    while queue:
        node = queue.pop(0)
        # print(queue)
        if node == end:
            path = []
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return path
        # visited.add(node)
        for neighbor in get_neighbors(maze, node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    return None


def get_neighbors(maze, node):
    neighbors = []
    rows, cols = maze.shape
    deltas = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    for delta in deltas:
        neighbor = (node[0] + delta[0], node[1] + delta[1])
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor] in [0, 2, 3]:
            neighbors.append(neighbor)
    return neighbors


# 连接路径方法
def combine_paths(maze, start, treasures, end):
    total_path = []
    current_position = start

    while treasures:
        shortest_path_length = float('inf')
        shortest_path_index = -1
        shortest_path = []

        for i, treasure in enumerate(treasures):
            # 使用广度优先搜索（BFS）找到当前位置到宝藏的最短路径
            path = bfs(maze, current_position, treasure)
            # print("PATH: ",path)
            if path and len(path) < shortest_path_length:
                shortest_path_length = len(path)
                shortest_path_index = i
                shortest_path = path
            # print("Shortest: ", shortest_path)

        if shortest_path:
            # 将最短路径添加到总路径中
            #  用[1:]可以防止新的路径头部和总路径的尾部相同，造成之后转弯判断出问题
            total_path.extend(shortest_path[1:])
            current_position = treasures[shortest_path_index]
            treasures.pop(shortest_path_index)
        else:
            treasures.pop(shortest_path_index)

    last_path = bfs(maze, current_position, end)

    if last_path:
        total_path.extend(last_path[1:])

    return total_path


# 绘制路径方法
def drew_shortest_path(maze, start, treasures, end):
    path = combine_paths(maze, start, treasures, end)
    if path is None:
        print('nothing')
    else:
        for position in path:
            # 将路径上的位置标记为2，以便在绘图中显示
            maze[position] = 2
    plot_maze(maze)


def judge_T_corner(maze):
    rows, cols = maze.shape
    corner_coordinate = []
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if maze[i][j] == 0:
                # 检查上方是否有墙
                if maze[i - 1][j] == 1:
                    # 检查左右两侧是否都是墙
                    if maze[i][j - 1] == 0 and maze[i][j + 1] == 0 and maze[i + 1][j] == 0:
                        corner_coordinate.append((i, j))
                # 检查下方是否有墙
                elif maze[i + 1][j] == 1:
                    # 检查左右两侧是否都是墙
                    if maze[i][j - 1] == 0 and maze[i][j + 1] == 0 and maze[i - 1][j] == 0:
                        corner_coordinate.append((i, j))
                # 检查左侧是否有墙
                elif maze[i][j - 1] == 1:
                    # 检查上下两侧是否都是墙
                    if maze[i - 1][j] == 0 and maze[i + 1][j] == 0 and maze[i][j + 1] == 0:
                        corner_coordinate.append((i, j))
                # 检查右侧是否有墙
                elif maze[i][j + 1] == 1:
                    # 检查上下两侧是否都是墙
                    if maze[i - 1][j] == 0 and maze[i + 1][j] == 0 and maze[i][j - 1] == 0:
                        corner_coordinate.append((i, j))
    return corner_coordinate


def judge_cross_corner(maze):
    rows, cols = maze.shape

    cross_coordinate = []

    for i in range(1, rows - 1):

        for j in range(1, cols - 1):
            if maze[i][j] == 0:
                if maze[i][j - 1] == 0 and maze[i][j + 1] == 0 and maze[i + 1][j] == 0 and maze[i - 1][j] == 0:
                    # 将十字拐角的坐标添加到列表中
                    cross_coordinate.append((i, j))
    return cross_coordinate


def is_turn_required(path, index):
    # 判断路径中是否需要转弯
    if index in [0, len(path) - 1]:
        return False

    x, y = path[index]
    prev_x, prev_y = path[index - 1]
    next_x, next_y = path[index + 1]

    if x == prev_x == next_x or y == prev_y == next_y:
        return False
    return True


# None Treasures_mark feedback
def get_turn_points(path, t_corner, cross_corner):
    turn_points = []

    for i in range(len(path)):
        if is_turn_required(path, i):

            current_point = path[i]
            prev_point = path[i - 1]
            next_point = path[i + 1]

            # 计算矢量差值
            vector_prev = (current_point[0] - prev_point[0], current_point[1] - prev_point[1])
            vector_next = (next_point[0] - current_point[0], next_point[1] - current_point[1])

            # 判断左转弯或右转弯
            cross_product = vector_prev[0] * vector_next[1] - vector_prev[1] * vector_next[0]
            turn_direction = None
            # 左转为1
            if cross_product > 0:
                turn_direction = '01'
            # 右转为2
            elif cross_product < 0:
                turn_direction = '02'

            if turn_direction:
                turn_points.append(turn_direction)

        # t拐角和十字拐角如果直行为3
        if path[i] in t_corner and not is_turn_required(path, i):
            turn_points.append('03')

        if path[i] in cross_corner and not is_turn_required(path, i):
            turn_points.append('03')

    return turn_points


def get_turn_points_else(maze, path, t_corner, cross_corner, treasures):
    turn_points = []
    visited_treasures = set()  # Keep track of visited treasures

    for i in range(len(path)):
        if path[i] in treasures:
            if path[i] not in visited_treasures:  # Check if treasure has been visited
                turn_points.append('06')
                visited_treasures.add(path[i])

        if is_turn_required(path, i):
            current_point = path[i]
            prev_point = path[i - 1]
            next_point = path[i + 1]

            # 计算矢量差值
            vector_prev = (current_point[0] - prev_point[0], current_point[1] - prev_point[1])
            vector_next = (next_point[0] - current_point[0], next_point[1] - current_point[1])

            # 判断左转弯或右转弯
            cross_product = vector_prev[0] * vector_next[1] - vector_prev[1] * vector_next[0]
            turn_direction = None
            # 左转为1
            if cross_product > 0:
                turn_direction = '01'
            # 右转为2
            elif cross_product < 0:
                turn_direction = '02'

            if turn_direction:
                turn_points.append(turn_direction)

        if i > 0 and i < len(path) - 1 and path[i - 1] == path[i + 1]:
            x, y = path[i]

            # 计算小车当前位置与掉头点的矢量差

            if path[i - 1][1] - path[i][1] == -1:  # 向右移动
                if maze[x - 1, y] == 1:  # 朝上转向
                    turn_points.append('07')
                elif maze[x + 1, y] == 1:  # 朝下转向
                    turn_points.append('08')
            elif path[i - 1][1] - path[i][1] == 1:  # 向左移动
                if maze[x + 1, y] == 1:  # 朝下转向
                    turn_points.append('07')
                elif maze[x - 1, y] == 1:  # 朝上转向
                    turn_points.append('08')
            elif path[i - 1][0] - path[i][0] == -1:  # 向下移动
                if maze[x, y - 1] == 1:  # 朝左转向
                    turn_points.append('08')
                elif maze[x, y + 1] == 1:  # 朝右转向
                    turn_points.append('07')
            elif path[i - 1][0] - path[i][0] == 1:  # 向上移动
                if maze[x, y + 1] == 1:  # 朝右转向
                    turn_points.append('08')
                elif maze[x, y - 1] == 1:  # 朝左转向
                    turn_points.append('07')

        # t拐角和十字拐角如果直行为1
        if path[i] in t_corner and not is_turn_required(path, i):
            turn_points.append('03')

        if path[i] in cross_corner and not is_turn_required(path, i):
            turn_points.append('03')

    return turn_points