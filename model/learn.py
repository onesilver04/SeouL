import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# npy 파일 로드
file_path_apt = 'npy/apt_data_with_string_label.npy'
file_path_hospital = 'npy/hospital_data_with_string_label.npy'
file_path_pharmacy = 'npy/pharmacy_data_with_string_label.npy'
file_path_kindergarten = 'npy/kindergarten_data_with_string_label.npy'
file_path_school = 'npy/school_data_with_string_label.npy'

apt_data = np.load(file_path_apt, allow_pickle=True)
hospital_data = np.load(file_path_hospital, allow_pickle=True)
pharmacy_data = np.load(file_path_pharmacy, allow_pickle=True)
kindergarten_data = np.load(file_path_kindergarten, allow_pickle=True)
school_data = np.load(file_path_school, allow_pickle=True)

# 데이터 합치기
all_data = np.vstack((apt_data, hospital_data, pharmacy_data, kindergarten_data, school_data))

# 특성과 라벨 분리
X = all_data[:, :-1].astype(float)  # 특성 데이터
y = all_data[:, -1]  # 라벨 데이터

# 라벨 인코딩 (문자열 -> 정수)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 데이터 나누기 (학습 및 테스트)
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 데이터 형태 변경 (LSTM 입력에 맞게)
X_train_reshaped = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test_reshaped = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# 모델 정의
model = Sequential()
model.add(LSTM(64, input_shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2]), return_sequences=True))
model.add(Dropout(0.5))  # 첫 번째 드롭아웃 추가
model.add(LSTM(64))
model.add(Dropout(0.5))  # 두 번째 드롭아웃 추가
model.add(Dense(32, activation='relu'))
model.add(Dense(len(np.unique(y_encoded)), activation='softmax'))

# 모델 컴파일
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 조기 종료 콜백 설정
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# 모델 학습
history = model.fit(X_train_reshaped, y_train, epochs=50, validation_data=(X_test_reshaped, y_test), callbacks=[early_stopping])

# 모델 저장
model.save('model/my_lstm_model_151.h5')

# 저장된 모델 불러오기
loaded_model = tf.keras.models.load_model('model/my_lstm_model_151.h5')

# 모델 평가
loss, accuracy = loaded_model.evaluate(X_test_reshaped, y_test)
print(f"Test Accuracy: {accuracy}")

# 학습 정확도 및 손실 그래프 그리기
plt.figure(figsize=(12, 4))

# 학습 및 검증 정확도
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# 학습 및 검증 손실
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

# 혼동 행렬 및 분류 보고서
y_pred = loaded_model.predict(X_test_reshaped)
y_pred_classes = np.argmax(y_pred, axis=1)

# 혼동 행렬 생성
cm = confusion_matrix(y_test, y_pred_classes)

# 혼동 행렬 시각화
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# 분류 보고서 출력
print(classification_report(y_test, y_pred_classes, target_names=label_encoder.classes_))