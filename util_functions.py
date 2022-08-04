import math

import cv2
import numpy as np
from convex_polygon_intersection import _sort_vertices_anti_clockwise_and_remove_duplicates, intersect


def millisecond_to_time(milliseconds):
    # print out time
    seconds = milliseconds // 1000
    milli_part = milliseconds % 1000
    minutes = 0
    hours = 0
    if seconds >= 60:
        minutes = seconds // 60
        seconds = seconds % 60
    if minutes >= 60:
        hours = minutes // 60
        minutes = minutes % 60
    return hours, minutes, seconds, milli_part


def center(x1, y1, x2, y2):
    """
    find the center of two points
    """
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return int(cx), int(cy)


def bottom_center(x1, y1, x2, y2):
    """
    find the center of rectangle box
    """
    cx = (x1 + x2) / 2
    cy = y2
    return int(cx), int(cy)


def bottom_foot_rect(x1, y1, x2, y2):
    # print("x1:", x1)
    # print("y1:", y1)
    # print("x2:", x2)
    # print("y2:", y2)
    offset_y = (y2 - y1) * 0.2
    # print("offset_y:", offset_y)

    # print("big rect area size:", cv2.contourArea(np.array([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], np.int32)))
    # print("small rect area size:", cv2.contourArea(np.array([(x1, y2), (x1, y2 - offset_y), (x2, y2 - offset_y), (x2, y2)], np.int32)))
    # print("intersect polygon area:", intersect_polygon_area([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], [(x1, y2), (x1, y2 - offset_y), (x2, y2 - offset_y), (x2, y2)]))
    return [(x1, y2 - offset_y), (x2, y2 - offset_y), (x2, y2), (x1, y2)]


def check_on_line_same_side(target_point, indicator_point, x1, y1, x2, y2):

    # print("target_point:", target_point, "-----indicator point:", indicator_point)
    # print("(", x1, y1, "), (", x2, y2, ")")

    indicator_x, indicator_y = indicator_point
    target_x, target_y = target_point
    indicator_result = (indicator_x - x2) * (y1 - y2) / (x1 - x2) + y2 - indicator_y
    target_result = (target_x - x2) * (y1 - y2) / (x1 - x2) + y2 - target_y
    if (indicator_result > 0 and target_result > 0) or (indicator_result < 0 and target_result < 0):
        return True
    else:
        return False


def bottom_foot_rect_area(point_list):
    a = point_list[2][0] - point_list[0][0]
    b = point_list[2][1] - point_list[0][1]
    return a * b

def get_rect_data(filename):
    with open(filename, "r", encoding="utf8") as f:
        contents = f.read().split("\n")
    return contents

def get_rect_size(rect_coordinates):
    result_rect_size = abs(rect_coordinates[0] - rect_coordinates[2]) * abs(
        rect_coordinates[1] - rect_coordinates[3])  # 矩形大小， 长*宽
    return result_rect_size

def merge_together_rect_one_round(pair_list):
    first_round_result = []
    i = 0
    while i < len(pair_list) - 1:
        together_rect_set = set()
        together_rect_set.update(pair_list[i])
        j = i + 1

        while j < len(pair_list):
            if together_rect_set.intersection(set(pair_list[j])):
                together_rect_set.update(pair_list[j])
                i += 1
            elif i == len(pair_list) - 2 and j == len(pair_list) - 1:
                first_round_result.append(set(pair_list[j]))
            j += 1
        # if len(together_rect_set) > len(pair_list[i]):
        first_round_result.append(together_rect_set)
        i += 1

    return first_round_result

def merge_together_rect(pair_list):
    if len(pair_list) == 1:
        return [set(pair_list[0])]
    result = merge_together_rect_one_round(pair_list)
    print(result)
    if len(result) == 1:
        return result
    final_result = merge_together_rect_one_round(result)
    return final_result

def check_point_location_to_parabola(point, coefficient):
    x = point[0]
    y = point[1]
    a = coefficient[0]
    b = coefficient[1]
    c = coefficient[2]
    """check point is above, below or on parabola"""
    temp = a * x * x + b * x + c
    if y > temp:  # above current parabola
        return "below"  # 因为y坐标轴向下，所以方向是反的
    elif y < temp:  # below current parabola
        return "above"  # 因为y坐标轴向下，所以方向是反的
    else:  # on parabola
        return "on"

def min_distance_of_rectangles(rect1_left_x, rect1_left_y, rect1_right_x, rect1_right_y, rect2_left_x, rect2_left_y, rect2_right_x, rect2_right_y):
    min_dict = 0

    # 首先计算两个矩形中心点

    C1_x = (rect1_left_x + rect1_right_x) / 2
    C1_y = (rect1_left_y + rect1_right_y) / 2
    C2_x = (rect2_left_x + rect2_right_x) / 2
    C2_y = (rect2_left_y + rect2_right_y) / 2

    rect1_width = rect1_right_x - rect1_left_x
    rect1_height = rect1_right_y - rect1_left_y
    rect2_width = rect2_right_x - rect2_left_x
    rect2_height = rect2_right_y - rect2_left_y

    # 分别计算两矩形中心点在X轴和Y轴方向的距离
    Dx = abs(C2_x - C1_x)
    Dy = abs(C2_y - C1_y)
    if (Dx < ((rect1_width + rect2_width) / 2)) and (Dy >= ((rect1_height + rect2_height) / 2)):# 两矩形不相交，在X轴方向有部分重合的两个矩形，最小距离是上矩形的下边线与下矩形的上边线之间的距离
        min_dist = Dy - ((rect1_height + rect2_height) / 2)
    elif (Dx >= ((rect1_width + rect2_width) / 2)) and (Dy < ((rect1_height + rect2_height) / 2)):# 两矩形不相交，在Y轴方向有部分重合的两个矩形，最小距离是左矩形的右边线与右矩形的左边线之间的距离
        min_dist = Dx - ((rect1_width + rect2_width) / 2)
    elif (Dx >= ((rect1_width + rect2_width) / 2)) and (Dy >= ((rect1_height + rect2_height) / 2)): # 两矩形不相交，在X轴和Y轴方向无重合的两个矩形，最小距离是距离最近的两个顶点之间的距离，利用勾股定理，很容易算出这一距离
        delta_x = Dx - ((rect1_width + rect2_width) / 2)
        delta_y = Dy - ((rect1_height + rect2_height) / 2)
        min_dist = math.sqrt(delta_x * delta_x + delta_y * delta_y)

    else: # 两矩形相交，最小距离为负值，返回 - 1
        min_dist = -1

    return min_dist
# def check_point_location_to_line(x, y, x1, y1, x2, y2):
#     pass
#
# def intersection_points_with_bottom_foot_rect():
#     pass



def cross_product(point1, point2):
    """向量积"""
    return point1[0] * point2[1] - point2[0] * point1[1]


def point_in_region(point, point_list):  # point: (x, y) point_list: [(x, y), (), ()...]
    """判断点在凸多边形内部还是外部"""
    if len(point_list) < 3:  # 至少3个点
        return False

    """向量法"""
    pre_cross = 0
    next_cross = 0
    v1 = []
    v2 = []
    v3 = []
    for i in range(len(point_list)):
        i_next = (i + 1) % len(point_list)
        i2_next = (i_next + 1) % len(point_list)

        v1 = (point_list[i][0] - point[0], point_list[i][1] - point[1])
        v2 = (point_list[i_next][0] - point[0], point_list[i_next][1] - point[1])
        v3 = (point_list[i2_next][0] - point[0], point_list[i2_next][1] - point[1])
        pre_cross = cross_product(v1, v2)
        next_cross = cross_product(v2, v3)

        if pre_cross * next_cross < 0:
            return False

    return True

    """顶点数量判断法"""
    # number_count = 0
    # for i in range(len(point_list)):  # 遍历多边形每个顶点
        # p1 = point_list[i]
        # p2 = point_list[(i + 1) % len(point_list)]  # p1是当前顶点，p2是下一个顶点
        #
        # if p1[1] == p2[1]:  # 如果这条边是水平的，跳过
        #     continue
        # if point[1] < min(p1[1], p2[1]):  # 如果目标点低于这个线段，跳过
        #     continue
        # if point[1] >= max(p1[1], p2[1]):  # 如果目标点高于这个线段，跳过
        #     continue
        #
        # x = (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
        # if x > point[0]:
        #     number_count += 1
    # if number_count % 2 == 1:
    #     return True  # 如果是奇数，说明在多边形里
    # else:
    #     return False  # 否则在多边形外 或 边上


def rect_in_region(rect_point_list, region_point_list):
    rect_in_region_flag = True
    for rect_point in rect_point_list:
        if not point_in_region(rect_point, region_point_list):
            rect_in_region_flag = False

    return rect_in_region_flag

def getPolygonArea(point_list):
    '''
    brief: calculate the Polygon Area with vertex coordinates
    :param points: list, input vertex coordinates
    :return: float, polygon area
    '''

    sizep = len(point_list)
    if sizep<3:
        return 0.0

    area = point_list[-1][0] * point_list[0][1] - point_list[0][0] * point_list[-1][1]
    for i in range(1, sizep):
        v = i - 1
        area += (point_list[v][0] * point_list[i][1])
        area -= (point_list[i][0] * point_list[v][1])

    return abs(0.5 * area)


def intersect_polygon_area(point_list1, point_list2):
    polygon1 = _sort_vertices_anti_clockwise_and_remove_duplicates(point_list1)
    polygon2 = _sort_vertices_anti_clockwise_and_remove_duplicates(point_list2)
    polygon3 = intersect(polygon1, polygon2)
    # print(polygon3)
    area_result = getPolygonArea(polygon3)
    # print("intersection poly area:", area_result)
    return area_result
    # cv2.contourArea()


"""--------------special functions for points based---------------"""


def distance_between_two_points(x1, y1, x2, y2):

    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def centers_for_rect_area(rect_coordinates):
    x1, y1, x2, y2 = rect_coordinates[0], rect_coordinates[1], rect_coordinates[2], rect_coordinates[3]

    offset_y = (y2 - y1) * 0.2
    offset_y_prime = (y2 - y1) * 0

    head_area_center_point = (int((x1 + x2) / 2), int((y1 + y1 + offset_y) / 2))
    waist_area_center_point = (int((x1 + x2) / 2), int((y1 + y2) / 2 + offset_y_prime))
    bottom_area_center_point = (int((x1 + x2) / 2), int((y2 - offset_y + y2) / 2))
    return head_area_center_point, waist_area_center_point, bottom_area_center_point


def check_min_distance_to_points(point, point_list_dict):
    min_dist_result = -1
    key_result = ""
    for key, temp_point_list in point_list_dict.items():
        for temp in temp_point_list:
            temp_dist_result = distance_between_two_points(point[0], point[1], temp[0], temp[1])
            if min_dist_result == -1:
                min_dist_result = temp_dist_result
                key_result = key
            if temp_dist_result < min_dist_result:
                min_dist_result = temp_dist_result
                key_result = key

    return key_result


if __name__ == '__main__':
    # print(bottom_foot_rect_area([(2,2), (2,6), (6,6),(2,6)]))

    """test rect min distance"""
    # rect1 = [200, 200, 500, 500]
    # rect2 = [600, 100, 900, 300]
    # rect3 = [700, 600, 800, 700]
    # rect4 = [100, 400, 300, 600]
    #
    # my_list = [rect2, rect3, rect4]
    #
    # for temp in my_list:
    #     print(min_distance_of_rectangles(rect1_left_x=rect1[0], rect1_left_y=rect1[1], rect1_right_x=rect1[2], rect1_right_y=rect1[3],
    #                                rect2_left_x=temp[0], rect2_left_y=temp[1], rect2_right_x=temp[2], rect2_right_y=temp[3]))
    """test together rect"""
    # first_1 = merge_together_rect([(0, 1), (1, 2), (3, 5), (3, 4), (5, 6), (7, 8), (9, 10), (3, 10)])
    # first_2 = merge_together_rect([(0, 1), (1, 2), (3, 5), (3, 4), (7, 3)])
    # first_3 = merge_together_rect([(0, 1), (1, 2), (3, 5), (3, 4), (2, 3)])
    first_4 = merge_together_rect([(0, 1), (0, 2)])
    # print(first_1)
    # print(merge_together_rect(first_1))
    # print(first_2)
    # print(merge_together_rect(first_2))
    # print(first_3)
    # print(merge_together_rect(first_3))
    print(first_4) # TODO

