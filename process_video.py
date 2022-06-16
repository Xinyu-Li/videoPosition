import cv2
import numpy as np
from draw_main_location import draw_main_locations

line_height = 700

offset = 10

def center(x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return int(cx), int(cy)


def bottom_center(x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    cy = y2
    return int(cx), int (cy)


def get_rect_data():
    with open("rect_result.txt", "r", encoding="utf8") as f:
        contents = f.read().split("\n")
    return contents


def get_parabola_coefficient(X0, Y0, X1, Y1, X2, Y2):
    A = (Y0 - Y1) / ((X0 - X1) * (X0 - X2)) - (Y1 - Y2) / ((X1 - X2) * (X0 - X2))
    B = (Y0 - Y1) / (X0 - X1) - ((X0 + X1) * (Y0 - Y1)) / ((X0 - X1) * (X0 - X2)) + (X0 + X1) * (Y1 - Y2) / ((X1 - X2) * (X0 - X2))
    C = Y0 - A * X0 * X0 - B * X0

    return A, B, C


def get_points_list(a, b, c):
    # x range 0~1280
    # y = a * x * x + b * x + c
    result = []
    for x in range(1281):
        y = a * x * x + b * x + c
        result.append((x, y))
    return result

def convert_millisecond_to_time(milliseconds):
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
    return (hours, minutes, seconds, milli_part)


def point_in_region(point, point_list):  # point: (x, y) point_list: [(x, y), (), ()...]
    number_count = 0
    for i in range(len(point_list)):  # 遍历多边形每个顶点
        p1 = point_list[i]
        p2 = point_list[(i + 1) % len(point_list)]  # p1是当前顶点，p2是下一个顶点

        if p1[1] == p2[1]:  # 如果这条边是水平的，跳过
            continue
        if point[1] < min(p1[1], p2[1]):  # 如果目标点低于这个线段，跳过
            continue
        if point[1] >= max(p1[1], p2[1]):  # 如果目标点高于这个线段，跳过
            continue

        x = (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
        if x > point[0]:
            number_count += 1
    if number_count % 2 == 1:
        return True  # 如果是奇数，说明在多边形里
    else:
        return False  # 否则在多边形外 或 边上



key_positions_list = ["phone", "ECG", "Meds", "b1 laptop", "b1 monitor", "b1 patient",
                      "b2 laptop", "b2 monitor", "b2 patient", "b2 oxygen",
                      "b3 laptop", "b3 monitor", "b3 patient", "b3 oxygen",
                      "b4 laptop", "b4 monitor", "b4 patient", "b4 oxygen",
                      "equip left", "equip right"]
def start_processing():
    cap = cv2.VideoCapture("C:\\develop\\videos\\processed_141_h264.mp4")
    contents = get_rect_data()
    count = 0
    wait_time = 21

    interact_b4_count = 0
    use_b4_laptop_count = 0

    pass_b4_count = 0
    pass_b4_laptop_count = 0

    interact_b4_frame_count = 0
    use_b4_laptop_frame_count = 0
    pass_b4_frame_count = 0
    pass_b4_laptop_frame_count = 0

    while True:
        ret, frame = cap.read()
        milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)
        if ret:

            draw_main_locations(frame)

            b4_pa_pts_list = [(795, 420), (835, 416), (901, 454), (867, 461)]
            b4_pa_pts = np.array(b4_pa_pts_list, np.int32)
            cv2.polylines(frame, [b4_pa_pts], True, (0, 0, 255))

            b4_lp_pts_list = [(865, 461), (894, 443), (917, 455), (966, 441), (977, 448), (888, 478)]
            b4_lp_pts = np.array(b4_lp_pts_list, np.int32)
            cv2.polylines(frame, [b4_lp_pts], True, (0, 0, 255))

            """----------------------------------画出每个rect的底部中点----------------------"""
            line = contents[count]
            rect_coordinates_list = eval(line.split(";;;")[1])
            for rect_coordinates in rect_coordinates_list:
                # print(rect_coordinates)
                center_point = bottom_center(rect_coordinates[0], rect_coordinates[1], rect_coordinates[2], rect_coordinates[3])
                result_size = abs(rect_coordinates[0] - rect_coordinates[2]) * abs(
                    rect_coordinates[1] - rect_coordinates[3])
                if result_size > 35000:
                    print(rect_coordinates, result_size)
                    cv2.circle(frame, center_point, 10, color=[0, 255, 255], thickness=-1)
                if point_in_region(center_point, b4_pa_pts_list):  # 判断是否在病床边上
                    interact_b4_frame_count += 1
                    pass_b4_frame_count += 1
                    cv2.putText(frame, "Passing Bed 4", (450, 580), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (255, 255, 50), 2)
                if point_in_region(center_point, b4_lp_pts_list):  # 判断是否在电脑边上
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



                # print(center_point)

                cv2.circle(frame, center_point, 5, color=[0, 0, 255], thickness=-1)
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

            a, b, c = get_parabola_coefficient(652, 513, 580, 508, 822, 503)
            # x range 0~1280
            # y = a * x * x + b * x + c
            pts_list = get_points_list(a, b, c)
            pa_pts = np.array(pts_list, np.int32)
            cv2.polylines(frame, [pa_pts], False, (0, 0, 255))

            # cv2.putText(frame, "Interact with Bed 4 : " + str(interact_b4_count), (80, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
            # cv2.putText(frame, "Pass Bed 4 : " + str(pass_b4_count), (450, 580), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.8, (255, 255, 50), 2)
            # cv2.putText(frame, "Use Bed 4 laptop : " + str(use_b4_laptop_count), (80, 660), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 50), 2)
            # cv2.putText(frame, "Pass Bed 4 laptop : " + str(pass_b4_laptop_count), (450, 660), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.8, (255, 255, 50), 2)
            cv2.putText(frame, "Time: %d:%d:%d.%d" % convert_millisecond_to_time(milliseconds), (80, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 50), 2)
            cv2.imshow('video', frame)

            count += 1

        key = cv2.waitKey(wait_time)
        if key == 27:  # Esc 退出
            break
        # elif key == ord('p') & 0xFF:
        elif key == 32:  # 空格键 暂停
            cv2.waitKey(0)
        elif key == ord(',') & 0xFF:  # left  slow down
            wait_time += 10
        elif key == ord('.') & 0xFF:  # right  speed up
            if wait_time > 10:
                wait_time -= 10
        # print(wait_time)


    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    start_processing()



