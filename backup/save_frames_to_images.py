import tkinter as tk

import cv2
import numpy as np

def save_frames():
    cap2 = cv2.VideoCapture("C:\\develop\\saved_data\\videos\\1111111_2.mp4")
    cap3 = cv2.VideoCapture("C:\\develop\\saved_data\\videos\\1111111_3.mp4")

    count = 0
    while True:
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        if ret2 and ret3:

            cv2.imwrite("C:\\develop\\saved_data\\videos\\images\\video_2_frame_" + str(count) + ".jpg", frame2)
            cv2.imwrite("C:\\develop\\saved_data\\videos\\images\\video_3_frame_" + str(count) + ".jpg", frame3)
            count += 1
            if count >= 200:
                break
        else:
            break

def test_tkinter():
    window = tk.Tk()
    greeting = tk.Label(text="Hello, Tkinter")
    greeting.pack()

    window.mainloop()