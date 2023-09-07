import json
import numpy as np
import matplotlib.pyplot as plt
import re

original_position_path = "C:\\develop\\videos\\141.json"
video_position_path = "C:\\develop\\videos\\track_141.txt"


def original_position_plot():
    with open(original_position_path, "r") as original_position_f:
        original_position_contents = original_position_f.read().split("\n")

    x_y_27261 = []  # GN2 - Graduate Nurse 2 - blue
    x_y_27226 = []  # GN1 - Graduate Nurse 1 - red
    x_y_27263 = []  # WN2 - Ward graduate nurse 2 - yellow
    x_y_27160 = []  # WN1 - Ward graduate nurse 1 - green
    x_y_27152 = []  # ACTOR - pink
    x_y_27234 = []  # Trolley ECG - black
    x_y_27154 = []  # Trolley Medicine - brown

    for line in original_position_contents:
        if line:
            line_obj = json.loads(line)[0]
            tagId = line_obj["tagId"]
            success = line_obj["success"]
            if not success:
                continue
            x = line_obj["data"]["coordinates"]["x"]
            y = line_obj["data"]["coordinates"]["y"]

            if tagId == "27226":
                x_y_27226.append((x, y))
            elif tagId == "27263":
                x_y_27263.append((x, y))
            elif tagId == "27261":
                x_y_27261.append((x, y))
            elif tagId == "27234":
                x_y_27234.append((x, y))
            elif tagId == "27154":
                x_y_27154.append((x, y))
            elif tagId == "27160":
                x_y_27160.append((x, y))
            elif tagId == "27152":
                x_y_27152.append((x, y))

    # list(zip(*x_y_27226))[0] # get the first element of all tuples.
    fig = plt.figure(figsize=(40, 40))
    plt.scatter(list(zip(*x_y_27226))[0], list(zip(*x_y_27226))[1], c="red")
    plt.scatter(list(zip(*x_y_27263))[0], list(zip(*x_y_27263))[1], c="yellow")
    plt.scatter(list(zip(*x_y_27261))[0], list(zip(*x_y_27261))[1], c="blue")
    plt.scatter(list(zip(*x_y_27234))[0], list(zip(*x_y_27234))[1], c="black")
    plt.scatter(list(zip(*x_y_27154))[0], list(zip(*x_y_27154))[1], c="brown")
    plt.scatter(list(zip(*x_y_27160))[0], list(zip(*x_y_27160))[1], c="green")
    plt.scatter(list(zip(*x_y_27152))[0], list(zip(*x_y_27152))[1], c="pink")

    plt.savefig("original_40x40.jpg")
    plt.show()

# 图片比例需要修改


def video_position_plot():
    with open(video_position_path, "r") as video_position_f:
        video_position_contents = video_position_f.read().split("\n")
    new_str = ""
    result_str = ""
    for line in video_position_contents:
        if "---------------" in line:
            result = re.findall("tensor\(.*?\)", new_str)
            rect_coordinates = re.findall("\[.*?\]\]", result[0])
            rect_ids = re.findall("\[.*?\]", result[2])

            rect_coordinates = eval(rect_coordinates[0])  # 矩形 左上 和 右下 点
            rect_ids = eval(rect_ids[0])  # 矩形的 id ，可能会变化多次
            print(rect_ids)
            print(rect_coordinates)  #
            result_str += (str(rect_ids) + ";;;" + str(rect_coordinates) + "\n")

            new_str = ""
            continue
        new_str += line.strip()
    with open("rect_result.txt", "w", encoding="utf8") as f:
        f.write(result_str)

# video_position_plot()

def calculate_rect_size():
    from backup.process_video import get_rect_data
    contents = get_rect_data()
    result_str = ""
    for line in contents:
        rect_coordinates_list = eval(line.split(";;;")[1])
        for rect_coordinates in rect_coordinates_list:
            result_size = abs(rect_coordinates[0] - rect_coordinates[2]) * abs(rect_coordinates[1] - rect_coordinates[3])
            print(result_size)
            result_str += (str(result_size) + "___")
        result_str += "-------------------\n"

    with open("rect_size.txt", "w", encoding="utf8") as f:
        f.write(result_str)

# calculate_rect_size()

def test_nested_loop():
    my_list = [0,1,2,3,4,5]
    for i in range(len(my_list) - 1):
        for j in range(i + 1, len(my_list)):
            print(my_list[i], "----", my_list[j])
        print("---------------------")

def test_flatten_list():
    my_list = [(1, 2), (0, 1), (2, 3)]
    result = np.array(my_list).flatten().tolist()
    print(result)

# test_flatten_list()

def reformat_data():
    with open("process_tracking_box/output_data/temporal_data.csv", "r", encoding="utf8") as f:
        contents = f.read().split("\n")
    result = ""
    for line in contents:
        if line:
            eles = line.split(";;;")
            result += (eles[0] + "," + eles[1] + "," + eles[2] + "," + eles[3] + "," \
                      + eles[4] + "," + eles[5] + "," + eles[6] + "," + eles[7] + "," \
                      + eles[8] + "," + eles[9] + "," + eles[10] + "," + eles[11] + "," \
                      + eles[12] + "\n")
    with open("process_tracking_box/output_data/temporal_data2.csv", "w", encoding="utf8") as f2:
        f2.write(result)

reformat_data()