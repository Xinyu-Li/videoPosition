def process_tracking_files():
    with open("tracking_box_data/track_144.txt", "r", encoding="utf8") as f:
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
    with open("tracking_box_data/track_144_processed.txt", "w", encoding="utf8") as f:
        f.write("\n".join(all_frame_tracking_boxes_str_list))
    print(count)
if __name__ == '__main__':
    # print("qerqerqerqer]])]"[:-2])
    process_tracking_files()
