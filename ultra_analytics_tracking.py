import supervision as sv
from ultralytics import YOLO
import numpy as np
import cv2
import torch


model = YOLO('yolov8s.pt')
# model = YOLO('yolov8m.pt')
# model = YOLO('yolov8l.pt')
# model = YOLO('yolov8x.pt')

model.to("cuda")


# Open the video file
input_video_path = ""
output_video_path = ""
output_rect_path = ""

cap = cv2.VideoCapture(input_video_path)

# Define the codec using VideoWriter_fourcc and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"MP4V")
out = cv2.VideoWriter(output_video_path, fourcc, 9, (2592, 1952))  # '1' denotes FPS. Modify as needed.


frame_count = 0
rect_result_list = []

# cv2.CAP_PROP_FRAME_COUNT  # total frame count
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    frame_count += 1
    print("{}/{}".format(frame_count,cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        rect_result_list.append(str(results[0].boxes.xywh) + "")  # can also use xyxy format
        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        # cv2.imshow("YOLOv8 Tracking", annotated_frame)
        out.write(annotated_frame)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

with open(output_rect_path, "w", encoding="utf8") as f:
    f.write("\n".join(rect_result_list))

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
