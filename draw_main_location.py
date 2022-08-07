import cv2
import numpy as np


def draw_main_locations(frame):
    """---------------------------------基准线------------------------------------------"""

    # cv2.line(frame, (10, line_height), (1200, line_height), (255, 255, 0), 3)
    # cv2.line(frame, (1180, 10), (1180, 710), (255, 255, 0), 3)
    # cv2.line(frame, (1, 1), (1180, 1), (255, 255, 0), 3)

    """---------------------------------画出主要标识点-------------------------------"""
    # Floor plan, 7057, 9464  # 整个场地大小，长和宽

    # Phone, 2886, 9283
    cv2.putText(frame, "phone", (1100, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.circle(frame, (1120, 360), 5, color=[0, 255, 255], thickness=-1)
    # ECG, 6542, 5988
    cv2.putText(frame, "ECG", (671, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.circle(frame, (671, 365), 5, color=[0, 255, 255], thickness=-1)
    # Meds, 6442, 5018
    cv2.putText(frame, "Meds", (720, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.circle(frame, (740, 380), 5, color=[0, 255, 255], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B1 laptop, 4564, 7589
    cv2.putText(frame, "B1 lp", (965, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (159, 255, 84), 2)
    cv2.circle(frame, (965, 400), 5, color=[159, 255, 84], thickness=-1)
    # B1 centre, 5496, 7589
    # B1 monitor, 6820, 6820
    cv2.putText(frame, "B1 mo", (1210, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (159, 255, 84), 2)
    cv2.circle(frame, (1250, 440), 5, color=[159, 255, 84], thickness=-1)
    # B1 oxygen, 6781, 8336
    """cannot see"""
    # B1 patient, 5911, 7589
    cv2.putText(frame, "B1 pa", (1120, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (159, 255, 84), 2)
    cv2.circle(frame, (1120, 450), 5, color=[159, 255, 84], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B2 laptop, 2478, 6581
    cv2.putText(frame, "B2 lp", (420, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (420, 420), 5, color=[240, 32, 160], thickness=-1)
    # B2 centre, 1547, 6581
    # B2 monitor, 223, 5834
    cv2.putText(frame, "B2 mo", (80, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (80, 400), 5, color=[240, 32, 160], thickness=-1)
    # B2 oxygen, 292, 7358
    cv2.putText(frame, "B2 ox", (10, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (10, 330), 5, color=[240, 32, 160], thickness=-1)
    # B2 patient, 1124, 6581
    cv2.putText(frame, "B2 pa", (200, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (200, 470), 5, color=[240, 32, 160], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B3 laptop, 4564, 3156
    cv2.putText(frame, "B3 lp", (560, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (565, 370), 5, color=[255, 118, 72], thickness=-1)
    # B3 centre, 5480, 3156
    # B3 monitor, 6827, 2371
    cv2.putText(frame, "B3 mo", (550, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (570, 310), 5, color=[255, 118, 72], thickness=-1)
    # B3 oxygen, 6827, 3895
    cv2.putText(frame, "B3 ox", (635, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (635, 310), 5, color=[255, 118, 72], thickness=-1)
    # B3 patient, 5911, 3156
    cv2.putText(frame, "B3 pa", (580, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (580, 345), 5, color=[255, 118, 72], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B4 laptop, 2478, 2802
    cv2.putText(frame, "B4 lp", (920, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (920, 365), 5, color=[255, 187, 255], thickness=-1)
    # B4 centre, 1539, 2802
    # B4 monitor, 223, 2047
    cv2.putText(frame, "B4 mo", (810, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (830, 315), 5, color=[255, 187, 255], thickness=-1)
    # B4 oxygen, 285, 3541
    cv2.putText(frame, "B4 ox", (880, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (880, 320), 5, color=[255, 187, 255], thickness=-1)
    # B4 patient, 1293, 2802
    cv2.putText(frame, "B4 pa", (850, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (870, 365), 5, color=[255, 187, 255], thickness=-1)

    # Equip left, 1155, 292
    cv2.putText(frame, "Eq left", (410, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 50), 2)
    cv2.circle(frame, (410, 350), 5, color=[255, 255, 50], thickness=-1)
    # Equip right, 5819, 292
    cv2.putText(frame, "Eq right", (130, 365), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 50), 2)
    cv2.circle(frame, (130, 385), 5, color=[255, 255, 50], thickness=-1)

    """---------------------------------------------------------------------------"""


def get_parabola_coefficient(X0, Y0, X1, Y1, X2, Y2):
    """
    based on three points, find the parabola coefficient
    """
    A = (Y0 - Y1) / ((X0 - X1) * (X0 - X2)) - (Y1 - Y2) / ((X1 - X2) * (X0 - X2))
    B = (Y0 - Y1) / (X0 - X1) - ((X0 + X1) * (Y0 - Y1)) / ((X0 - X1) * (X0 - X2)) + (X0 + X1) * (Y1 - Y2) / ((X1 - X2) * (X0 - X2))
    C = Y0 - A * X0 * X0 - B * X0

    return A, B, C


def get_points_list(a, b, c):
    """
    based on parabola coefficient, get all points in this parabola
    """
    # x range 0~1280
    # y = a * x * x + b * x + c
    result = []
    for x in range(300, 1080):  # 根据视频size (720 * 1280) 得到的值
        y = a * x * x + b * x + c
        # if x == 698 or x == 572 or x == 755 or x == 955 or x == 938 or x == 1027 or x == 867:
        # print(x, y)
        result.append((x, y))
    return result


def draw_main_areas(frame, parabola_pts_list, parabola_coefficient):
    """--------------------------半场分割-----------------------------------------
    根据地砖线条，手动选取三个点，计算出parabola 系数
    """

    if not parabola_pts_list:
        a, b, c = get_parabola_coefficient(652, 513, 580, 508, 822, 503)
        parabola_coefficient.append(a)
        parabola_coefficient.append(b)
        parabola_coefficient.append(c)
        # x range 0~1280
        # y = a * x * x + b * x + c
        parabola_pts_list.extend(get_points_list(a, b, c))

    cv2.polylines(frame, [np.array(parabola_pts_list, np.int32)], False, (0, 0, 255))

    """----------------------------Bed 1 laptop area------------------------------"""
    bed1_laptop_pts_list = [(855, 493), (881, 530), (994, 490), (973, 465)]
    bed1_laptop_pts = np.array(bed1_laptop_pts_list, np.int32)
    cv2.polylines(frame, [bed1_laptop_pts], True, (159, 255, 84))

    """-------------------------------Bed 1 area----------------------------------
    use middle line and parabola to check
    """

    bed1_bed2_middle_line = [(685, 513), (685, 720)]
    cv2.line(frame, (685, 513), (685, 720), (0, 255, 255))

    # temp_point = (1, 1)
    # result_for_bed1 = check_point_location_to_parabola(temp_point[0], temp_point[1], a, b, c)
    # if result_for_bed1 == "above":
    # # could be
    # elif result_for_bed1 == "below":
    #
    # else:

    """---------------------------Bed 2 or Eq right area--------------------------
    use parabola and x < 330 to check
    """

    """------------------------------Bed 2 area-----------------------------------
    use middle line and parabola to check
    """

    """----------------------------Bed 2 laptop area------------------------------"""
    bed2_laptop_pts_list = [(519, 512), (482, 541), (383, 511), (416, 489)]
    bed2_laptop_pts = np.array(bed2_laptop_pts_list, np.int32)
    cv2.polylines(frame, [bed2_laptop_pts], True, (240, 32, 160))

    """-------------------------Bed 3 with family member area---------------------
    use parabola and bed3_eq_left_line to check
    """
    bed3_eq_left_line = [(508, 410), (407, 476)]
    cv2.line(frame, (508, 410), (407, 476), (255, 118, 72))
    """-------------------------------Eq left area--------------------------------
    use parabola and bed3_eq_left_line to check
    """

    """------------------------------Bed 3 laptop area----------------------------"""
    bed3_laptop_pts_list = [(489, 482), (511, 453), (589, 463), (577, 497)]
    bed3_laptop_pts = np.array(bed3_laptop_pts_list, np.int32)
    cv2.polylines(frame, [bed3_laptop_pts], True, (255, 118, 72))

    """--------------------------------ECG area------------------------------------

    """
    # bed3_and_ecg_pts_list = [(582, 493), (610, 440), (720, 447), (750, 500)]
    bed3_and_ecg_pts_list = [(638, 417), (710, 417), (717, 437), (634, 417)]
    bed3_and_ecg_pts = np.array(bed3_and_ecg_pts_list, np.int32)
    cv2.polylines(frame, [bed3_and_ecg_pts], True, (0, 255, 255))

    """-----------------------------Bed 3 area close to Meds and ECG------------------------------------"""
    bed3_patient_line = [(690, 415), (698, 513)]

    cv2.line(frame, (690, 415), (698, 513), (255, 118, 72))

    """----------------------------Meds area------------------------------"""
    meds_pts_list = [(807, 437), (717, 437), (710, 417), (785, 415)]
    meds_pts = np.array(meds_pts_list, np.int32)
    cv2.polylines(frame, [meds_pts], False, (0, 255, 255))

    """-------------------------------Bed 4 area----------------------------------
    use parabola line and bed4 line to check
    """
    # b4_patient_pts_list = [(802, 415), (838, 415), (901, 454), (867, 461)]
    # b4_patient_pts = np.array(b4_patient_pts_list, np.int32)
    # cv2.polylines(frame, [b4_patient_pts], True, (0, 0, 255))
    bed4_patient_line = [(785, 415), (867, 495)]
    cv2.line(frame, (785, 415), (867, 495), (255, 187, 255))

    """-------------------------------Bed 4 laptop--------------------------------"""
    bed4_laptop_pts_list = [(927, 473), (897, 455), (993, 430), (1018, 446)]
    bed4_laptop_pts = np.array(bed4_laptop_pts_list, np.int32)
    cv2.polylines(frame, [bed4_laptop_pts], True, (255, 187, 255))

    """-------------------------------phone area----------------------------------"""
    phone_pts_list = [(1030, 325), (1030, 450), (1165, 450), (1165, 325)]
    phone_pts = np.array(phone_pts_list, np.int32)
    cv2.polylines(frame, [phone_pts], True, (0, 255, 255))

    return bed1_laptop_pts_list, bed2_laptop_pts_list, bed3_laptop_pts_list, bed4_laptop_pts_list, \
           bed3_and_ecg_pts_list, meds_pts_list, phone_pts_list, \
           bed1_bed2_middle_line, bed3_eq_left_line, bed3_patient_line, bed4_patient_line
