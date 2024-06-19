import cv2
import mediapipe as mp
import pandas as pd

def extract_hand_landmarks(video_path, output_csv_path):
    # MediaPipe 손 모델 초기화
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # 동영상 파일 열기
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Failed to open the video file: {video_path}")
        return
    
    frame_count = 0
    hand_landmarks_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_landmarks_dict = {"frame": frame_count}
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    hand_landmarks_dict[f"x{idx}"] = landmark.x
                    hand_landmarks_dict[f"y{idx}"] = landmark.y
                    hand_landmarks_dict[f"z{idx}"] = landmark.z
                hand_landmarks_list.append(hand_landmarks_dict)

    cap.release()
    hands.close()

    # DataFrame으로 변환 후 CSV 파일로 저장
    df = pd.DataFrame(hand_landmarks_list)
    df.to_csv(output_csv_path, index=False)
    print(f"Hand landmarks saved to {output_csv_path}")

# 사용 예시
video_path = 'school6.avi'  # 동영상 파일 경로를 지정하세요.
output_csv_path = 'hand_landmarks/school_6.csv'  # 저장할 CSV 파일 경로를 지정하세요.
extract_hand_landmarks(video_path, output_csv_path)

