import os


def process_tracking_files(rect_path, processed_rect_path):
    with open(rect_path, "r", encoding="utf8") as f:
        contents = f.read().split("\n")

    one_frame_tracking_box_flag = False
    one_frame_tracking_boxes_str = ""
    all_frame_tracking_boxes_str_list = []
    count = 0
    for line in contents:
        if "-------------------------------------------------" == line:
            count += 1
        if line.startswith("[array([["):
            one_frame_tracking_boxes_str += line[7:]
            one_frame_tracking_box_flag = True
            continue

        if one_frame_tracking_box_flag:
            one_frame_tracking_boxes_str += line
        if line.endswith("]])]"):
            all_frame_tracking_boxes_str_list.append(str(eval(one_frame_tracking_boxes_str[:-2])))
            # print(eval(one_frame_tracking_boxes_str[:-2]))
            one_frame_tracking_boxes_str = ""
            one_frame_tracking_box_flag = False
    with open(processed_rect_path, "w", encoding="utf8") as f:
        f.write("\n".join(all_frame_tracking_boxes_str_list))
    print(count)


if __name__ == '__main__':
    # print("qerqerqerqer]])]"[:-2])
    for i in range(141, 219):
        rect_path = "tracking_box_data/track_" + str(i) + ".txt"
        processed_rect_path = "tracking_box_data/track_" + str(i) + "_processed.txt"
        if os.path.exists(rect_path):
            process_tracking_files(rect_path=rect_path, processed_rect_path=processed_rect_path)
        else:
            print("track_" + str(i) + ".txt not exist")
