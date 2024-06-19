from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageFont, ImageDraw, Image
import time
import threading

app = Flask(__name__)

# 수어 단어 리스트
words = ['병원', '약국', '아파트', '학교', '유치원']

# 모델 로드
model = load_model('my_lstm_model.h5')

# MediaPipe Hands 초기화
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 한글 폰트 설정
fontpath = "C:/WINDOWS/Fonts/MALANGMALANGR.TTF"  # 사용할 한글 폰트 경로
font = ImageFont.truetype(fontpath, 32)

# 손가락 관절 마디 색상 설정
landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)  # 노란색으로 설정
connection_drawing_spec = mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)  # 파란색으로 설정

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 웹캠 피드를 Flask 응답으로 변환하는 제너레이터 함수
def generate_frames():
    # 초기 변수 설정
    landmark_history = []
    capture_duration = 2  # 데이터 수집 시간 (초)
    last_capture_time = time.time()
    predicted_word = ""  # 마지막으로 예측된 단어
    last_predicted_time = time.time()  # 마지막 예측 시간이 저장된 변수

    with mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

       while cap.isOpened():
        # 프레임 읽기
        success, image = cap.read()
        if not success:
            continue

        # 이미지를 RGB로 변환하고 좌우 반전
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # 손 인식 결과 받기
        results = hands.process(image)

        # 이미지를 다시 BGR로 변환 (OpenCV는 BGR을 사용)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                landmark_history.append(landmarks)

                mp_drawing.draw_landmarks(    
                    image,     
                    hand_landmarks,     
                    mp_hands.HAND_CONNECTIONS,     
                    landmark_drawing_spec,    
                    connection_drawing_spec    
                )

        # 일정 시간 동안 데이터를 수집한 후 예측 수행
        current_time = time.time()
        if current_time - last_capture_time >= capture_duration:
            if landmark_history:
                # 평균 랜드마크 계산
                avg_landmarks = np.mean(landmark_history, axis=0)
                avg_landmarks = np.expand_dims(avg_landmarks, axis=0)

                # 모델 예측
                prediction = model.predict(avg_landmarks)
                predicted_label = np.argmax(prediction, axis=1)[0]
                predicted_word = words[predicted_label]
                last_predicted_time = current_time  # 마지막 예측 시간을 업데이트
            else:
                predicted_word = ""

            # 다음 예측을 위해 초기화
            landmark_history = []
            last_capture_time = current_time

        # 예측된 단어를 화면에 계속 표시
        if predicted_word and (current_time - last_predicted_time <= capture_duration):
            image_pil = Image.fromarray(image)
            draw = ImageDraw.Draw(image_pil)
            draw.text((200, 400), f'Prediction: {predicted_word}', font=font, fill=(255, 255, 255))
            image = np.array(image_pil)

        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_language')
def sign_language():
    return render_template('sign_language.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)