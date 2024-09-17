import cv2
import os

video_file = input("Enter the name of the video file: 输入视频文件名称 ")

if not os.path.isfile(video_file) or not video_file.endswith('.mp4'):
    print("The file does not exist or is not an MP4 file. 文件不存在或不是mp4")
    exit()

id_string = input("Enter an ID string: 输入命名用ID")
frame_rate = float(input("Enter the frame rate: 输入帧率"))

output_dir = input("Enter the output directory: 输入保存文件夹目录")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

cap = cv2.VideoCapture(video_file)

video_frame_rate = cap.get(cv2.CAP_PROP_FPS)

if frame_rate > video_frame_rate:
    frame_rate = video_frame_rate

original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

desired_width = 480
desired_height = 270

interval = int(video_frame_rate / frame_rate)

frame_count = 0
saved_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    if frame.shape[1] != desired_width or frame.shape[0] != desired_height:
        frame = cv2.resize(frame, (desired_width, desired_height))
    
    if frame_count % interval == 0:
        output_path = os.path.join(output_dir, f"{id_string}_{saved_count + 1}.jpg")
        cv2.imwrite(output_path, frame)
        saved_count += 1
    
    frame_count += 1

cap.release()

print(f"Extracted {saved_count} frames and saved to {output_dir}.")
print(f"已提取 {saved_count} 帧并保存到了 {output_dir}.")
