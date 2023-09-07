"""
ffmpeg -i "C:\develop\videos\h264_videos\_141_h264.mp4" -f image2 -r 1 "C:\develop\videos\h264_videos\frames\image-%3d.jpg"

ffmpeg -r 1 -f image2 -i "C:\develop\videos\h264_videos\frames\image-%3d.jpg" output.mp4
"""
import os.path
import subprocess

def get_frames_per_second(base_path, video_name_list):
    # for i in range(141, 219):
    #     original_video_path = r'C:\develop\videos\h264_videos\_' + str(i) + '_h264.mp4'
    #     each_frames_folder = r'C:\develop\videos\h264_videos\frames_' + str(i)
    for video_name in video_name_list:
        original_video_path = base_path + video_name
        each_frames_folder = base_path + "frames_" + video_name

        if os.path.exists(original_video_path):
            if not os.path.exists(each_frames_folder):
                os.mkdir(each_frames_folder)
            cmd_str = 'ffmpeg -i "' + original_video_path + '" -f image2 -r 1 "' + each_frames_folder + r'\image-%3d.jpg"'
            print(cmd_str)
            subprocess.run(cmd_str, shell=True)
        else:
            print(original_video_path, "not exist")


def generate_1_frame_video(base_path, video_name_list):

    # for i in range(141, 219):
    #     each_frames_folder = r'C:\develop\videos\h264_videos\frames_' + str(i)
    for video_name in video_name_list:
        each_frames_folder = base_path + "frames_" + video_name
        if os.path.exists(each_frames_folder):
            cmd_str = 'ffmpeg -r 1 -f image2 -i "' + each_frames_folder + r'\image-%3d.jpg" ' + each_frames_folder + r'\1_frame_' + str(i) + '.mp4'
            print(cmd_str)
            subprocess.run(cmd_str, shell=True)
        else:
            print(each_frames_folder, "frame folder not exist")


if __name__ == '__main__':
    base_path = ""
    video_name_list = []
    # every minute only get 1 frame
    get_frames_per_second(base_path, video_name_list)
    print("--------------------------------------------------------")
    # combine all frames to a video
    generate_1_frame_video(base_path, video_name_list)
