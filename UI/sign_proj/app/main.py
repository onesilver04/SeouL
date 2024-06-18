from flask import Flask, render_template, Response, jsonify

import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageFont, ImageDraw, Image
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
    with mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while True:
            success, image = cap.read()
            if not success:
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            highest_confidence = 0
            predicted_word = ""

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()

                    if len(landmarks) == model.input_shape[1]:
                        landmarks = np.expand_dims(landmarks, axis=0)
                        prediction = model.predict(landmarks)
                        predicted_label = np.argmax(prediction, axis=1)[0]
                        confidence = np.max(prediction)

                        if confidence > highest_confidence:
                            highest_confidence = confidence
                            predicted_word = words[predicted_label]

                    mp_drawing.draw_landmarks(
                        image, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS, 
                        landmark_drawing_spec,
                        connection_drawing_spec
                    )

            if predicted_word:
                image_pil = Image.fromarray(image)
                draw = ImageDraw.Draw(image_pil)
                draw.text((10, 30), f'Prediction: {predicted_word}', font=font, fill=(255, 255, 255, 0))
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
