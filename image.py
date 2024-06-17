import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

# 수어 단어 리스트
words = ['hospital', 'pharmacy', 'apartment', 'school', 'kindergarten']

# 모델 로드
model = load_model('model/my_lstm_model.h5')

# MediaPipe Hands 초기화
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 웹캠 열기
cap = cv2.VideoCapture(0)

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

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 손의 랜드마크 좌표를 배열로 변환
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                
                # 모델에 입력할 수 있도록 차원 추가
                if len(landmarks) == model.input_shape[1]:
                    landmarks = np.expand_dims(landmarks, axis=0)
                    
                    # 모델 예측
                    prediction = model.predict(landmarks)
                    predicted_label = np.argmax(prediction, axis=1)[0]

                    # 예측 결과 출력
                    cv2.putText(image, f'Prediction: {words[predicted_label]}', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # 손의 랜드마크 그리기
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # 화면에 출력
        cv2.imshow('Sign Language Recognition', image)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
