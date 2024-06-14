import cv2
import mediapipe as mp
import pandas as pd

# MediaPipe Hands 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 이미지 파일 경로
IMAGE_FILES = [f'apt10-{i}.jpg' for i in range(1, 15)]

# 데이터를 저장할 리스트 초기화
data = []

# MediaPipe Hands 사용
with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(IMAGE_FILES):
        # 이미지 읽기
        image = cv2.imread(file)
        if image is None:
            print(f'Image {file} not found.')
            continue

        # BGR 이미지를 RGB로 변환
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # 손 랜드마크가 검출된 경우
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 각 랜드마크 좌표를 리스트에 추가
                row = {'image': file}
                for i, landmark in enumerate(hand_landmarks.landmark):
                    row[f'x_{i}'] = landmark.x
                    row[f'y_{i}'] = landmark.y
                    row[f'z_{i}'] = landmark.z
                data.append(row)

# 데이터프레임 생성
df = pd.DataFrame(data)

# CSV 파일로 저장
df.to_csv('apt_hand_landmarks/hand_landmarks_apt10.csv', index=False)