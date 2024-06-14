import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# CSV 파일 읽기
df = pd.read_csv('apt_hand_landmarks/hand_landmarks_apt10.csv')

# 'image' 열 제거
df = df.drop(columns=['image'])

# 데이터프레임의 크기 확인
total_size = df.size
num_rows = df.shape[0]
num_cols = df.shape[1]

# 샘플 수와 특징 수 계산
num_samples = num_rows
num_features = num_cols

print(f"샘플 수: {num_samples}")
print(f"특징 수: {num_features}")

# 각 샘플의 프레임 수 계산
time_steps = total_size // (num_samples * num_features)

print(f"각 샘플의 프레임 수: {time_steps}")

# 데이터의 크기와 목표 형태가 맞는지 확인
if total_size == num_samples * time_steps * num_features:
    # 데이터를 (샘플 수, 시간 단계, 특징 수)로 reshape
    X = df.values.reshape(num_samples, time_steps, num_features)

    # 예시로 모든 샘플의 레이블이 1인 경우
    y = np.array([[1]] * X.shape[0])

    # 학습 데이터와 테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 전처리된 데이터 저장
    np.save('apt_npy/X_train_apt10.npy', X_train)
    np.save('apt_npy/X_test_apt10.npy', X_test)
    np.save('apt_npy/y_train_apt10.npy', y_train)
    np.save('apt_npy/y_test_apt10.npy', y_test)

    print("전처리 완료 및 파일 저장 완료: X_train.npy, X_test.npy, y_train.npy, y_test.npy")
else:
    print("데이터의 크기가 일치하지 않습니다. 프레임 수나 데이터 구조를 다시 확인하세요.")
