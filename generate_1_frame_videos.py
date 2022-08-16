"""
ffmpeg -i "C:\develop\videos\h264_videos\_141_h264.mp4" -f image2 -r 1 "C:\develop\videos\h264_videos\frames\image-%3d.jpg"

ffmpeg -r 1 -f image2 -i "C:\develop\videos\h264_videos\frames\image-%3d.jpg" output.mp4
"""
import os.path

import ffmpeg
import subprocess

def get_frames_per_second():
    for i in range(141, 219):
        original_video_path = r'C:\develop\videos\h264_videos\_' + str(i) + '_h264.mp4'
        each_frames_folder = r'C:\develop\videos\h264_videos\frames_' + str(i)

        if os.path.exists(original_video_path):
            if not os.path.exists(each_frames_folder):
                os.mkdir(each_frames_folder)
            cmd_str = 'ffmpeg -i "' + original_video_path + '" -f image2 -r 1 "' + each_frames_folder + r'\image-%3d.jpg"'
            print(cmd_str)
            subprocess.run(cmd_str, shell=True)
        else:
            print(original_video_path, "not exist")

def generate_1_frame_video():
    for i in range(141, 219):
        each_frames_folder = r'C:\develop\videos\h264_videos\frames_' + str(i)
        if os.path.exists(each_frames_folder):
            cmd_str = 'ffmpeg -r 1 -f image2 -i "' + each_frames_folder + r'\image-%3d.jpg" ' + each_frames_folder + r'\1_frame_' + str(i) + '.mp4'
            print(cmd_str)
            subprocess.run(cmd_str, shell=True)
        else:
            print(each_frames_folder, "frame folder not exist")
def test(a):
    print("helloworld")

if __name__ == '__main__':
    # get_frames_per_second()
    print("--------------------------------------------------------")
    # generate_1_frame_video()

    test()