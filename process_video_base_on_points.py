import os

import cv2
import numpy as np
from draw_main_location import draw_main_locations, draw_main_areas
from util_functions import *

# line_height = 700
#
# offset = 10


# key_positions_list = ["phone", "ECG", "Meds", "b1 laptop", "b1 monitor", "b1 patient",
#                       "b2 laptop", "b2 monitor", "b2 patient", "b2 oxygen",
#                       "b3 laptop", "b3 monitor", "b3 patient", "b3 oxygen",
#                       "b4 laptop", "b4 monitor", "b4 patient", "b4 oxygen",
#                       "equip right", "equip right"]



def start_processing(video_path, rect_path, output_path):
    # result_temporal_string = "time,bed1,bed2,bed3,bed4,bed1_lp,bed2_lp,bed3_lp,bed4_lp,eq_right,eq_right,ecg,meds,phone\n"
    result_temporal_string = "time,bed1,bed2,bed3,bed4,bed1_lp,bed2_lp,bed3_lp,bed4_lp,eq_right,eq_left,,phone\n"
    cap = cv2.VideoCapture(video_path)
    # contents = get_rect_data("rect_result.txt")
    contents = get_rect_data(rect_path)
    frame_count = 0

    wait_time = 1

    target_waist_point_list_dict = {"b1_lp": [(965, 400), (942, 407)], "b1_pa": [(1120, 450), (950, 450), (1035, 424), (1240, 539), (1200, 445)],
                                    "b2_lp": [(420, 420), (402, 421)], "b2_pa": [(200, 470), (417, 464), (325, 431), (69, 453)],
                                    "b3_lp": [(565, 370), (574, 381)], "b3_pa": [(580, 345), (597, 394), (616, 361), (530, 392)],
                                    "b4_lp": [(920, 365), (938, 374)], "b4_pa": [(870, 365), (840, 379), (895, 401), (889, 369)],
                                    # "ecg": [(671, 365)], "meds": [(724, 415), (756, 442)],
                                    "eq_right": [(399, 371), (435, 362)], "eq_left": [(119, 417), (167, 409)], "phone": [(1120, 360), (1120, 383)]}

    target_head_point_list_dict = {"b3_mo": [(570, 310)], "b3_ox": [(635, 310)], "b4_mo": [(830, 315)], "b4_ox": [(880, 320)], "phone": [(1120, 360), (1120, 383)]}

    while True:
        ret, frame = cap.read()
        milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)  # 获取每帧的时间戳

        if ret:
            draw_main_locations(frame)
            # bed1_laptop_pts_list, bed2_laptop_pts_list, bed3_laptop_pts_list, bed4_laptop_pts_list, bed3_and_ecg_pts_list, meds_pts_list, phone_pts_list, bed1_bed2_middle_line, bed3_eq_right_line, bed3_patient_line, bed4_patient_line = draw_main_areas(
            #     frame, parabola_pts_list, parabola_coefficient)

            """--------------------------------画出每个rect的底部中点-------------------------"""
            try:
                line = contents[frame_count]  # 获取每帧矩形坐标
            except:
                print("frame count different from rect count")
                break
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

            eq_right_count_rect = 0
            eq_left_count_rect = 0

            # ecg_count_rect = 0
            # meds_count_rect = 0

            phone_count_rect = 0

            people_together_count_rect = 0
            people_together_pair_list = []
            # print("---------------each frame---------------------------")
            for rect_coordinates in rect_coordinates_list:
                # print(rect_coordinates)
                head_area_center_point, waist_area_center_point, bottom_area_center_point = centers_for_rect_area(rect_coordinates)
                cv2.circle(frame, head_area_center_point, 5, color=[0, 0, 255], thickness=-1)
                cv2.circle(frame, waist_area_center_point, 5, color=[0, 0, 255], thickness=-1)
                cv2.circle(frame, bottom_area_center_point, 5, color=[0, 0, 255], thickness=-1)

                """如果bottom 矩形 3个点在 某区域内，则判定该人在该区域内"""

                """如果bottom 矩形 2个点在 某区域内，则求交点，并获取 多边形面积，再与矩形做比较"""

                # print("------------------")
                # if frame_count != 0 and frame_count % 40 == 0:  # 每40帧判断一次，检查了每个 矩形
                if frame_count != 0:
                    """判断bed1 laptop (965, 400) (942, 407)  用腰部点判断"""
                    """判断bed1 patient (1120, 450) (950, 450) (1035, 424) (1240, 539) (1200, 445) 用腰部点判断"""
                    # """判断bed1 monitor (1250, 440) 用腰部点判断"""

                    """判断bed2 laptop (420, 420) (402, 421) 用腰部点判断"""
                    """判断bed2 patient (200, 470) (417, 464) (325, 431) (69, 453) 用腰部点判断"""
                    # """判断bed2 monitor (80, 400) 用腰部点判断"""
                    # """判断bed2 ox (10, 330) 用头部点判断"""

                    """判断bed3 laptop (565, 370) (574, 381) 用腰部点判断"""
                    """判断bed3 patient (580, 345) (597, 394) (616, 361) (530, 392) 用腰部点判断"""

                    """判断bed4 laptop (920, 365) (938, 374) 用腰部点判断"""
                    """判断bed4 patient (870, 365) (840, 379) (895, 401) (889, 369) 用腰部点判断"""

                    """判断ecg (671, 365) 用腰部点判断"""
                    """判断meds (724, 365) (766, 358) 用腰部点判断"""
                    """判断eq right (399, 371) (435, 362) 用腰部点判断"""
                    """判断eq left (119, 417) (167, 409) 用腰部点判断"""



                    # """判断bed3 ox (635, 310) 用头部点判断"""
                    # """判断bed3 monitor (570, 310) 用头部点判断"""
                    # """判断bed4 monitor (830, 315) 用头部点判断"""
                    # """判断bed4 ox (880, 320) 用头部点判断"""
                    """判断phone (1120, 360) 用头部点判断"""






                    """先用腰部判定，再用头部判定覆盖腰部判定"""




                    result1 = check_min_distance_to_points(waist_area_center_point, target_waist_point_list_dict)
                    # result2 = check_min_distance_to_points(head_area_center_point, target_head_point_list_dict)

                    if result1 == "b1_lp":
                        bed1_laptop_count_rect += 1
                    elif result1 == "b1_pa":
                        bed1_patient_count_rect += 1
                    elif result1 == "b2_lp":
                        bed2_laptop_count_rect += 1
                    elif result1 == "b2_pa":
                        bed2_patient_count_rect += 1
                    elif result1 == "b3_lp":
                        bed3_laptop_count_rect += 1
                    elif result1 == "b3_pa":
                        bed3_patient_count_rect += 1
                    elif result1 == "b4_lp":
                        bed4_laptop_count_rect += 1
                    elif result1 == "b4_pa":
                        bed4_patient_count_rect += 1
                    # elif result1 == "ecg":
                    #     ecg_count_rect += 1
                    # elif result1 == "meds":
                    #     meds_count_rect += 1
                    elif result1 == "eq_right":
                        eq_right_count_rect += 1
                    elif result1 == "eq_left":
                        eq_left_count_rect += 1
                    elif result1 == "phone":
                        phone_count_rect += 1

            # if frame_count % 40 == 0:  # 每40帧判断一次，检查了每个 矩形
            if frame_count != 0:
                # print("time:", frame_count // 40, "Near bed 1 laptop--------number_people", bed1_laptop_count_rect)
                # print("time:", frame_count // 40, "Near bed 2 laptop--------number_people", bed2_laptop_count_rect)
                # print("time:", frame_count // 40, "Near bed 3 laptop--------number_people", bed3_laptop_count_rect)
                # print("time:", frame_count // 40, "Near bed 4 laptop--------number_people", bed4_laptop_count_rect)
                # print("time:", frame_count // 40, "Near phone---------------number_people", phone_count_rect)
                # print("time:", frame_count // 40, "Near ECG-----------------number_people", ecg_count_rect)
                # print("time:", frame_count // 40, "Near meds----------------number_people", meds_count_rect)

                # print("time:", frame_count // 40, "Near bed 1 patient-------number_people", bed1_patient_count_rect)
                # print("time:", frame_count // 40, "Near bed 2 patient-------number_people", bed2_patient_count_rect)
                # print("time:", frame_count // 40, "Near bed 3 patient-------number_people", bed3_patient_count_rect)
                # print("time:", frame_count // 40, "Near bed 4 patient-------number_people", bed4_patient_count_rect)
                # print("time:", frame_count // 40, "Near eq right-------------number_people", eq_right_count_rect)
                # print("time:", frame_count // 40, "Near eq left-------------number_people", eq_left_count_rect)

                """----------------------------------判断在一起的人-------------------------------"""
                # people_together_merge_result = merge_together_rect(people_together_pair_list)
                # print("people together: ", people_together_pair_list, "---merged:", people_together_merge_result)
                # print("------------------------------------------------------------------------------------------")

                # "time,bed1,bed2, bed3,bed4,bed1_lp, bed2_lp,bed3_lp,bed4_lp, eq_left,eq_right,ecg, meds,phone\n"

                result_temporal_string += str(frame_count // 40) + "," + str(bed1_patient_count_rect) + "," + \
                                          str(bed2_patient_count_rect) + "," + str(bed3_patient_count_rect) + "," + \
                                          str(bed4_patient_count_rect) + "," + str(bed1_laptop_count_rect) + "," + \
                                          str(bed2_laptop_count_rect) + "," + str(bed3_laptop_count_rect) + "," + \
                                          str(bed4_laptop_count_rect) + "," + str(eq_right_count_rect) + "," + \
                                          str(eq_left_count_rect) + "," + str(phone_count_rect) + "\n"

                # result_temporal_string += str(frame_count // 40) + "," + str(bed1_patient_count_rect) + "," + str(bed2_patient_count_rect) + "," + \
                #                           str(bed3_patient_count_rect) + "," + str(bed4_patient_count_rect) + "," + str(bed1_laptop_count_rect) + "," + \
                #                           str(bed2_laptop_count_rect) + "," + str(bed3_laptop_count_rect) + "," + str(bed4_laptop_count_rect) + "," + \
                #                           str(eq_right_count_rect) + "," + str(eq_left_count_rect) + "," + str(ecg_count_rect) + "," + \
                #                           str(meds_count_rect) + "," + str(phone_count_rect) + "\n"
                # if point_in_region(bottom_rect_center_point, bed3_laptop_pts_list):
                #     cv2.putText(frame, "Using bed 3 laptop", (450, 660), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)

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
    with open(output_path, "w", encoding="utf8") as f:
        f.write(result_temporal_string)


if __name__ == "__main__":
    for i in range(141, 219):

        if i > 140:
            video_path = "C:\\develop\\videos\\processed_1_frame_videos\\processed_1_frame_" + str(i) + ".mp4"
            rect_path = "process_tracking_box/tracking_box_data/track_" + str(i) + "_processed.txt"
            output_path = "process_tracking_box/output_data/1_frame_temporal_data_based_points_" + str(i) + ".csv"
            if os.path.exists(video_path):
                print("processing.......................", i)
                start_processing(video_path, rect_path, output_path)
            else:
                print("processed_1_frame_" + str(i) + ".mp4 not exist")
