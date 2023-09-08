import pickle
import cv2
import numpy as np
from fisheyewarping import FisheyeWarping  # code has bugs, need to fix load_dewarp_mesh() method


def build_mesh_file():

    fisheye_img = cv2.imread('./test-fisheye.jpg')
    frd = FisheyeWarping(fisheye_img, use_multiprocessing=False)
    frd.build_dewarp_mesh(save_path='./dewarp-mesh.pkl')
    frd.run_dewarp(save_path='./dewarp-output.png')


def convert_fisheye_video(input_video_path, output_video_path):
    DIM = (4071, 1296)  # output video width and height
    # video_path = "D:/PythonProjects/sample.mp4"

    # 对每一帧进行处理
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output_video_path, fourcc, 9, DIM)

    # Create a named window
    cv2.namedWindow('fisheye_video', cv2.WINDOW_NORMAL)

    # Resize the window
    cv2.resizeWindow('fisheye_video', 2040, 650)

    frame_count = 0
    while (cap.isOpened()):
        frame_count += 1
        ret, frame = cap.read()
        if not ret:
            break

        frd = FisheyeWarping(frame, use_multiprocessing=False)
        frd.load_dewarp_mesh(mesh_path='./dewarp-mesh.pkl')

        undistorted_frame = frd.run_dewarp()

        cv2.imshow("fisheye_video", undistorted_frame)
        out.write(undistorted_frame)

        print("{}/{}".format(frame_count, cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()

# step 1, run build
# build_mesh_file()

# step 2, comment run build function, add input video and output video path
convert_fisheye_video("../sample.mp4", "sample_fisheye_converted.mp4")
