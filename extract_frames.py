import cv2
import os

def extract_frames(video_path, output_folder, custom_name, frame_rate=30):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    count = 0
    success, image = video.read()

    if not success:
        print(f"Error: Unable to read video file {video_path}")
        return

    while success:
        if count % frame_rate == 0:
            frame_id = int(count / frame_rate) + 1
            output_path = os.path.join(output_folder, f"{custom_name}-{frame_id}.jpg")
            if cv2.imwrite(output_path, image):
                print(f"Saved frame {frame_id} to {output_path}")
            else:
                print(f"Error: Could not save frame {frame_id}")
        success, image = video.read()
        count += 1

    video.release()

if __name__ == "__main__":
    video_path = 'KETI_SL_0000007874.avi' #비디오 위치
    output_folder = 'output_frames'
    custom_name = 'hospital1' #저장할 파일 이름
    frame_rate = 5

    extract_frames(video_path, output_folder, custom_name, frame_rate)