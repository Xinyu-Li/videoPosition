import cv2
import numpy as np
from draw_main_location import draw_main_locations, draw_main_areas
from util_functions import *

# line_height = 700
#
# offset = 10


key_positions_list = ["phone", "ECG", "Meds", "b1 laptop", "b1 monitor", "b1 patient",
                      "b2 laptop", "b2 monitor", "b2 patient", "b2 oxygen",
                      "b3 laptop", "b3 monitor", "b3 patient", "b3 oxygen",
                      "b4 laptop", "b4 monitor", "b4 patient", "b4 oxygen",
                      "equip left", "equip right"]


def start_processing():
    result_temporal_string = "time;;;bed1;;;bed2;;;bed3;;;bed4;;;bed1_lp;;;bed2_lp;;;bed3_lp;;;bed4_lp;;;eq_left;;;ecg;;;meds;;;phone;;;people_together\n"
    cap = cv2.VideoCapture("C:\\develop\\videos\\processed_144_h264.mp4")
    # contents = get_rect_data("rect_result.txt")
    contents = get_rect_data("process_tracking_box/tracking_box_data/track_144_processed.txt")
    frame_count = 0

    wait_time = 21

    area_intersection_ratio = 0.3

    parabola_pts_list = []
    parabola_coefficient = []
    while True:
        ret, frame = cap.read()
        milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)  # 获取每帧的时间戳

        if ret:
            draw_main_locations(frame)
            bed1_laptop_pts_list, bed2_laptop_pts_list, bed3_laptop_pts_list, bed4_laptop_pts_list, bed3_and_ecg_pts_list, meds_pts_list, phone_pts_list, bed1_bed2_middle_line, bed3_eq_left_line, bed3_patient_line, bed4_patient_line = draw_main_areas(
                frame, parabola_pts_list, parabola_coefficient)

            """--------------------------------画出每个rect的底部中点-------------------------"""
            line = contents[frame_count]  # 获取每帧矩形坐标
            # rect_coordinates_list = eval(line.split(";;;")[1])  # only for 141
            rect_coordinates_list = [[item[1], item[2], item[3], item[4]] for item in eval(line)]
            bed1_laptop_count_rect = 0
            bed2_laptop_count_rect = 0
            bed3_laptop_count_rect = 0
            bed4_laptop_count_rect = 0

            bed1_patient_count_rect = 0
            bed2_patient_count_rect = 0
            bed3_patient_count_rect = 0
            bed4_patient_count_rect = 0

            eq_left_count_rect = 0

            ecg_count_rect = 0
            meds_count_rect = 0

            phone_count_rect = 0

            people_together_count_rect = 0
            people_together_pair_list = []
            # print("---------------each frame---------------------------")
            for rect_coordinates in rect_coordinates_list:
                # print(rect_coordinates)
                bottom_rect_center_point = bottom_center(rect_coordinates[0], rect_coordinates[1], rect_coordinates[2], rect_coordinates[3])
                bottom_foot_rect_point_list = bottom_foot_rect(rect_coordinates[0], rect_coordinates[1], rect_coordinates[2], rect_coordinates[3])
                bottom_foot_rect_area_value = bottom_foot_rect_area(bottom_foot_rect_point_list)

                cv2.circle(frame, bottom_rect_center_point, 5, color=[0, 0, 255], thickness=-1)
                cv2.polylines(frame, [np.array(bottom_foot_rect_point_list, np.int32)], True, [0, 0, 255])


                """如果bottom 矩形 3个点在 某区域内，则判定该人在该区域内"""


                """如果bottom 矩形 2个点在 某区域内，则求交点，并获取 多边形面积，再与矩形做比较"""


                # print("------------------")
                if frame_count != 0 and frame_count % 40 == 0:  # 每40帧判断一次，检查了每个 矩形

                    """判断bed1 laptop"""
                    intersect_polygon_area_bed1_laptop_value = intersect_polygon_area(bottom_foot_rect_point_list, bed1_laptop_pts_list)
                    if intersect_polygon_area_bed1_laptop_value > bottom_foot_rect_area_value * area_intersection_ratio:
                        cv2.putText(frame, "Near bed 1 laptop", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        bed1_laptop_count_rect += 1
                        continue

                    """判断bed2 laptop"""
                    intersect_polygon_area_bed2_laptop_value = intersect_polygon_area(bottom_foot_rect_point_list, bed2_laptop_pts_list)
                    if intersect_polygon_area_bed2_laptop_value > bottom_foot_rect_area_value * area_intersection_ratio:
                        cv2.putText(frame, "Near bed 2 laptop", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        bed2_laptop_count_rect += 1
                        continue

                    """判断bed3 laptop"""
                    intersect_polygon_area_bed3_laptop_value = intersect_polygon_area(bottom_foot_rect_point_list, bed3_laptop_pts_list)
                    if intersect_polygon_area_bed3_laptop_value > bottom_foot_rect_area_value * area_intersection_ratio:
                        cv2.putText(frame, "Near bed 3 laptop", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        bed3_laptop_count_rect += 1
                        continue

                    """判断bed4 laptop"""
                    intersect_polygon_area_bed4_laptop_value = intersect_polygon_area(bottom_foot_rect_point_list, bed4_laptop_pts_list)
                    if intersect_polygon_area_bed4_laptop_value > bottom_foot_rect_area_value * area_intersection_ratio:
                        cv2.putText(frame, "Near bed 4 laptop", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        bed4_laptop_count_rect += 1
                        continue

                    """判断phone"""
                    intersect_polygon_area_phone_value = intersect_polygon_area(bottom_foot_rect_point_list, phone_pts_list)
                    # print("bottom rect points:", bottom_foot_rect_point_list)
                    if intersect_polygon_area_phone_value > bottom_foot_rect_area_value * area_intersection_ratio:
                        cv2.putText(frame, "Near Phone", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        phone_count_rect += 1
                        continue

                    """判断ecg"""
                    intersect_polygon_area_ecg_value = intersect_polygon_area(bottom_foot_rect_point_list, bed3_and_ecg_pts_list)
                    if intersect_polygon_area_ecg_value > bottom_foot_rect_area_value * area_intersection_ratio:
                        cv2.putText(frame, "Near ECG", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        ecg_count_rect += 1
                        continue

                    """判断meds"""
                    intersect_polygon_area_meds_value = intersect_polygon_area(bottom_foot_rect_point_list, meds_pts_list)
                    if intersect_polygon_area_meds_value > bottom_foot_rect_area_value * area_intersection_ratio:
                        cv2.putText(frame, "Near meds", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        meds_count_rect += 1
                        continue


                    above_parabola_count_point = 0
                    below_parabola_count_point = 0
                    below_parabola_rect_point_list = []
                    above_parabola_rect_point_list = []
                    print(bottom_foot_rect_point_list)
                    for bottom_foot_rect_point in bottom_foot_rect_point_list:
                        result_position = check_point_location_to_parabola(bottom_foot_rect_point, parabola_coefficient)
                        # cv2.putText(frame, result_position + " parabola", (450, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                        # print(bottom_foot_rect_point, "-", result_position + " parabola", parabola_coefficient)
                        if result_position == "above":
                            above_parabola_count_point += 1
                            above_parabola_rect_point_list.append(bottom_foot_rect_point)
                        elif result_position == "below":
                            below_parabola_count_point += 1
                            below_parabola_rect_point_list.append(bottom_foot_rect_point)
                    # print("below_parabola_count_point :", below_parabola_count_point)
                    if below_parabola_count_point >= 3:  # 超过3个点 below
                        # "B1 pa", (1120, 430)
                        # "B2 pa", (200, 450)
                        # line: x = 685
                        line_equation_x = 685  # line equation between bed1 bed2
                        close_bed1_count_point = 0
                        close_bed2_count_point = 0
                        for bottom_foot_rect_point in below_parabola_rect_point_list:
                            if bottom_foot_rect_point[0] > line_equation_x:
                                close_bed1_count_point += 1
                            else:
                                close_bed2_count_point += 1

                        if close_bed1_count_point >= 3:
                            bed1_patient_count_rect += 1  # 表明rect 在bed 1
                        elif close_bed1_count_point == 2:
                            intersect_polygon_close_bed2_area_value = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                             [bottom_foot_rect_point_list[0],
                                                                                              (line_equation_x, bottom_foot_rect_point_list[0][1]),
                                                                                              (line_equation_x, bottom_foot_rect_point_list[3][1]),
                                                                                              bottom_foot_rect_point_list[3]])
                            if intersect_polygon_close_bed2_area_value > bottom_foot_rect_area_value * 0.5:
                                bed2_patient_count_rect += 1  # 表明rect 超过一半 在bed 2
                            else:
                                bed1_patient_count_rect += 1  # 表明rect 超过一半 在bed 1
                        else:
                            bed2_patient_count_rect += 1  # 表明rect 在bed 2
                    elif below_parabola_count_point == 2:
                        line_equation_x = 685  # line equation between bed1 bed2
                        close_bed1_count_point = 0
                        close_bed2_count_point = 0
                        for bottom_foot_rect_point in [bottom_foot_rect_point_list[2], bottom_foot_rect_point_list[3]]:
                            if bottom_foot_rect_point[0] > line_equation_x:
                                close_bed1_count_point += 1
                            else:
                                close_bed2_count_point += 1

                        if close_bed1_count_point == 2:  # 两点都靠近bed 1
                            temp_x1 = bottom_foot_rect_point_list[3][0]
                            temp_x2 = bottom_foot_rect_point_list[2][0]
                            temp_y1 = -0.0005300329498190461 * temp_x1 * temp_x1 + 0.7224450386215091 * temp_x1 + 267.28496191865185
                            temp_y2 = -0.0005300329498190461 * temp_x2 * temp_x2 + 0.7224450386215091 * temp_x2 + 267.28496191865185
                            intersect_polygon_close_bed1_area_value = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                             [(temp_x1, temp_y1), (temp_x2, temp_y2),
                                                                                              bottom_foot_rect_point_list[2],
                                                                                              bottom_foot_rect_point_list[3]])
                            if intersect_polygon_close_bed1_area_value > bottom_foot_rect_area_value * 0.5:
                                bed1_patient_count_rect += 1  # 表明rect 超过一半 在bed 1
                            else:
                                if check_on_line_same_side(bottom_foot_rect_point_list[0], (850, 345), x1=785, y1=415, x2=867, y2=495):  # 因为是长方形，如果第一个点在，则另一个点必在
                                    bed4_patient_count_rect += 1
                                elif not check_on_line_same_side(bottom_foot_rect_point_list[0], (850, 345), x1=785, y1=415, x2=867, y2=495) \
                                        and check_on_line_same_side(bottom_foot_rect_point_list[1], (850, 345), x1=785, y1=415, x2=867, y2=495):
                                    temp_x = (bottom_foot_rect_point_list[0][1] - 495) * (785 - 867) / (415 - 495) + 867
                                    intersect_polygon_close_bed4_area_value1 = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                                      [(temp_x, bottom_foot_rect_point_list[0][1]),
                                                                                                       bottom_foot_rect_point_list[1],
                                                                                                       (temp_x2, temp_y2), (867, 495)])

                                    intersect_polygon_close_bed4_area_value2 = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                                      [bottom_foot_rect_point_list[0],
                                                                                                       (temp_x, bottom_foot_rect_point_list[0][1]),
                                                                                                       (867, 495), (temp_x1, temp_y1)])
                                    if intersect_polygon_close_bed4_area_value1 > intersect_polygon_close_bed4_area_value2:
                                        bed4_patient_count_rect += 1
                                    else:
                                        # ignore the rect
                                        pass
                        elif close_bed1_count_point == 1:  # 1点都靠近bed 1, 1点靠近bed 2
                            pass  # 处于交叉点位置，判定不属于任何bed
                        else:  # 两点都靠近bed 2
                            temp_x1 = bottom_foot_rect_point_list[3][0]
                            temp_x2 = bottom_foot_rect_point_list[2][0]
                            temp_y1 = -0.0005300329498190461 * temp_x1 * temp_x1 + 0.7224450386215091 * temp_x1 + 267.28496191865185
                            temp_y2 = -0.0005300329498190461 * temp_x2 * temp_x2 + 0.7224450386215091 * temp_x2 + 267.28496191865185
                            intersect_polygon_close_bed2_area_value = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                             [(temp_x1, temp_y1), (temp_x2, temp_y2),
                                                                                              bottom_foot_rect_point_list[2],
                                                                                              bottom_foot_rect_point_list[3]])
                            if intersect_polygon_close_bed2_area_value > bottom_foot_rect_area_value * 0.5:
                                bed2_patient_count_rect += 1  # 表明rect 超过一半 在bed 2
                            else:
                                if check_on_line_same_side(bottom_foot_rect_point_list[1], (410, 330), x1=516, y1=410, x2=442,
                                                           y2=483):  # 因为是长方形，如果第一个点在，则另一个点必在
                                    eq_left_count_rect += 1
                                elif not check_on_line_same_side(bottom_foot_rect_point_list[1], (410, 330), x1=516, y1=410, x2=442,
                                                                 y2=483) and check_on_line_same_side(bottom_foot_rect_point_list[0], (410, 330),
                                                                                                     x1=516, y1=410, x2=442, y2=483):

                                    temp_x = (bottom_foot_rect_point_list[0][1] - 483) * (516 - 442) / (410 - 483) + 442

                                    intersect_polygon_close_bed3_area_value1 = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                                      [(temp_x, bottom_foot_rect_point_list[0][1]),
                                                                                                       bottom_foot_rect_point_list[1],
                                                                                                       (temp_x2, temp_y2), (442, 483)])

                                    intersect_polygon_close_bed3_area_value2 = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                                      [bottom_foot_rect_point_list[0],
                                                                                                       (temp_x, bottom_foot_rect_point_list[0][1]),
                                                                                                       (442, 483), (temp_x1, temp_y1)])
                                    if intersect_polygon_close_bed3_area_value1 > intersect_polygon_close_bed3_area_value2:
                                        bed3_patient_count_rect += 1
                                    else:
                                        eq_left_count_rect += 1
                                else:
                                    bed3_patient_count_rect += 1
                    else:  # 超过3个点 above
                        print("has rect above:", above_parabola_rect_point_list)
                        close_eq_left_count_point = 0
                        close_bed3_count_point = 0
                        close_bed4_count_point = 0

                        # "Eq left", (410, 330)
                        # bed3_eq_left_line = [(x1=508, y1=410), (x2=407, y2=476)]
                        # (410 - 407)  * (410 - 483) / (516 - 442) + 483 - 330 = 184.567567568 > 0
                        # "B3 pa", (580, 335)
                        # bed3_patient_line = [(x1=690, y1=415), (x2=698, y2=513)]
                        # bed4_patient_line = [(x1=785, y1=415), (x2=867, y2=495)]
                        # "B4 pa", (850, 345)
                        for bottom_foot_rect_point in bottom_foot_rect_point_list:
                            if check_on_line_same_side(bottom_foot_rect_point, (410, 330), x1=508, y1=410, x2=407, y2=476):
                                close_eq_left_count_point += 1
                            elif check_on_line_same_side(bottom_foot_rect_point, (850, 345), x1=785, y1=415, x2=867, y2=495):
                                close_bed4_count_point += 1
                            elif check_on_line_same_side(bottom_foot_rect_point, (580, 400), x1=508, y1=410, x2=407,
                                                         y2=476) and check_on_line_same_side(bottom_foot_rect_point, (580, 400), x1=690, y1=415,
                                                                                             x2=698, y2=513):
                                close_bed3_count_point += 1
                        print("close_eq_left_count_point:", close_eq_left_count_point)
                        print("close_bed4_count_point:", close_bed4_count_point)
                        print("close_bed3_count_point:", close_bed3_count_point)
                        if close_eq_left_count_point >= 3:
                            eq_left_count_rect += 1
                        elif close_bed4_count_point >= 2:
                            bed4_patient_count_rect += 1
                        elif close_bed3_count_point >= 3:
                            bed3_patient_count_rect += 1
                        elif close_eq_left_count_point == 2:
                            temp_x2 = (bottom_foot_rect_point_list[0][1] - 476) * (508 - 407) / (410 - 476) + 407
                            temp_x3 = (bottom_foot_rect_point_list[3][1] - 476) * (508 - 407) / (410 - 476) + 407
                            intersect_polygon_close_eq_left_area_value = intersect_polygon_area(bottom_foot_rect_point_list,
                                                                                                [bottom_foot_rect_point_list[0],
                                                                                                 (temp_x2, bottom_foot_rect_point_list[0][1]),
                                                                                                 (temp_x3, bottom_foot_rect_point_list[3][1]),
                                                                                                 bottom_foot_rect_point_list[3]])
                            if intersect_polygon_close_eq_left_area_value > bottom_foot_rect_area_value * 0.5:
                                eq_left_count_rect += 1  # 表明rect 超过一半 在eq left
                            else:
                                bed3_patient_count_rect += 1  # 表明rect 超过一半 在bed 3
                        elif close_bed3_count_point == 2:
                            bed3_patient_count_rect += 1



            if frame_count % 40 == 0:  # 每40帧判断一次，检查了每个 矩形
                print("time:", frame_count // 40, "Near bed 1 laptop--------number_people", bed1_laptop_count_rect)
                print("time:", frame_count // 40, "Near bed 2 laptop--------number_people", bed2_laptop_count_rect)
                print("time:", frame_count // 40, "Near bed 3 laptop--------number_people", bed3_laptop_count_rect)
                print("time:", frame_count // 40, "Near bed 4 laptop--------number_people", bed4_laptop_count_rect)
                print("time:", frame_count // 40, "Near phone---------------number_people", phone_count_rect)
                print("time:", frame_count // 40, "Near ECG-----------------number_people", ecg_count_rect)
                print("time:", frame_count // 40, "Near meds----------------number_people", meds_count_rect)

                print("time:", frame_count // 40, "Near bed 1 patient-------number_people", bed1_patient_count_rect)
                print("time:", frame_count // 40, "Near bed 2 patient-------number_people", bed2_patient_count_rect)
                print("time:", frame_count // 40, "Near bed 3 patient-------number_people", bed3_patient_count_rect)
                print("time:", frame_count // 40, "Near bed 4 patient-------number_people", bed4_patient_count_rect)
                print("time:", frame_count // 40, "Near eq left-------------number_people", eq_left_count_rect)


                for i in range(len(rect_coordinates_list) - 1):
                    for j in range(i + 1, len(rect_coordinates_list)):
                        rect1 = rect_coordinates_list[i]
                        rect2 = rect_coordinates_list[j]
                        min_dist_value = min_distance_of_rectangles(
                            rect1_left_x=rect1[0], rect1_left_y=rect1[1], rect1_right_x=rect1[2], rect1_right_y=rect1[3],
                            rect2_left_x=rect2[0], rect2_left_y=rect2[1], rect2_right_x=rect2[2], rect2_right_y=rect2[3])
                        rect1_size_result = get_rect_size(rect1)
                        rect2_size_result = get_rect_size(rect2)
                        # print("rect1 area size:", rect1_size_result, "-------rect2 area size:", rect2_size_result, "-----min dist:", min_dist_value)

                        if min_dist_value < 80 and abs(rect1_size_result - rect2_size_result) < 3000:
                            # print(i, j)
                            people_together_pair_list.append((i, j))
                people_together_merge_result = merge_together_rect(people_together_pair_list)
                print("people together: ", people_together_pair_list, "---merged:", people_together_merge_result)
                print("------------------------------------------------------------------------------------------")

                "time,bed1,bed2,bed3,bed4,bed1_lp,bed2_lp,bed3_lp,bed4_lp,eq_left,ecg,meds,phone,people_together\n"
                result_temporal_string += str(frame_count // 40) + ";;;" + \
                                          str(bed1_patient_count_rect) + ";;;" + str(bed2_patient_count_rect) + ";;;" + \
                                          str(bed3_patient_count_rect) + ";;;" + str(bed4_patient_count_rect) + ";;;" + \
                                          str(bed1_laptop_count_rect) + ";;;" + str(bed2_laptop_count_rect) + ";;;" + \
                                          str(bed3_laptop_count_rect) + ";;;" + str(bed4_laptop_count_rect) + ";;;" + \
                                          str(eq_left_count_rect) + ";;;" + str(ecg_count_rect) + ";;;" + str(meds_count_rect) + ";;;" + \
                                          str(phone_count_rect) + ";;;" + str(people_together_merge_result) + "\n"
                # if point_in_region(bottom_rect_center_point, bed3_laptop_pts_list):
                #     cv2.putText(frame, "Using bed 3 laptop", (450, 660), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)

            """
                if result_size > 35000:
                    print(rect_coordinates, result_size)
                    cv2.circle(frame, center_point, 10, color=[0, 255, 255], thickness=-1)


                if point_in_region(center_point, b4_patient_pts_list):  # 判断是否在病床边上
                    interact_b4_frame_count += 1
                    pass_b4_frame_count += 1
                    cv2.putText(frame, "Passing Bed 4", (450, 580), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (255, 255, 50), 2)
                if point_in_region(center_point, b4_laptop_pts_list):  # 判断是否在电脑边上
                    use_b4_laptop_frame_count += 1
                    pass_b4_laptop_frame_count += 1
                    cv2.putText(frame, "Passing Bed 4 laptop", (450, 660),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (255, 255, 50), 2)

                # 判断有问题 TODO
                if interact_b4_frame_count > 120:  # 超过3秒
                    interact_b4_count += 1
                    cv2.putText(frame, "Interacting with Bed 4", (80, 580),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                    interact_b4_frame_count = 0
                if pass_b4_frame_count > 120:
                    pass_b4_count += 1

                if use_b4_laptop_frame_count > 120:
                    use_b4_laptop_count += 1
                    cv2.putText(frame, "Using Bed 4 laptop", (80, 660),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
                    use_b4_laptop_frame_count = 0
                if pass_b4_laptop_frame_count > 120:
                    pass_b4_laptop_count += 1
                """

            # print(center_point)

            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            """-----------------------------------target----------------------------------
                1. 是否在交谈
                2. 接近了哪个仪器
                3. 接近了哪个床
                4. 是否使用电脑
            """

            # 停留超过3秒，120帧画面，才判断为在该位置 停留

            # 如果被遮挡，则需要判断遮挡前的位置，然后预估现在位置

            # 判断接近 -》 先出现遮挡 -》 判断停留时间 -》 再判断脚底位置

            # 根据连续矩形大小-》判断移动方向

            # 矩形小到一定尺寸，又和bed 有重合 -》 在该bed床边

            # cv2.putText(frame, "reach phone", (100, 650), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # cv2.putText(frame, "Interact with Bed 4 : " + str(interact_b4_count), (80, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
            # cv2.putText(frame, "Pass Bed 4 : " + str(pass_b4_count), (450, 580), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.8, (255, 255, 50), 2)
            # cv2.putText(frame, "Use Bed 4 laptop : " + str(use_b4_laptop_count), (80, 660), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
            # cv2.putText(frame, "Pass Bed 4 laptop : " + str(pass_b4_laptop_count), (450, 660), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.8, (255, 255, 50), 2)
            cv2.putText(frame, "Time: %d:%d:%d.%d" % millisecond_to_time(milliseconds), (80, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 50), 2)
            cv2.imshow('video', frame)

            frame_count += 1

        key = cv2.waitKey(wait_time)
        if key == 27:  # Esc exit
            break
        # elif key == ord('p') & 0xFF:
        elif key == 32:  # whitespace pause
            cv2.waitKey(0)
        elif key == ord(',') & 0xFF:  # left  slow down
            wait_time += 10
            print("wait time:", wait_time)
        elif key == ord('.') & 0xFF:  # right  speed up
            if wait_time > 10:
                wait_time -= 10
                print("wait time:", wait_time)
        # print(wait_time)

        if not ret:
            break
    print("frame_count:", frame_count)

    cv2.destroyAllWindows()
    cap.release()
    with open("temporal_data.csv", "w", encoding="utf8") as f:
        f.write(result_temporal_string)


if __name__ == "__main__":
    start_processing()
