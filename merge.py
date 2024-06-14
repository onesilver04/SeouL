import numpy as np
import glob
import os

npy_dir = 'apt_npy'

# npy 파일 리스트 가져오기
X_train_files = glob.glob(os.path.join(npy_dir, 'X_train_apt*.npy'))
X_test_files = glob.glob(os.path.join(npy_dir, 'X_test_apt*.npy'))
y_train_files = glob.glob(os.path.join(npy_dir, 'y_train_apt*.npy'))
y_test_files = glob.glob(os.path.join(npy_dir, 'y_test_apt*.npy'))

# npy 파일 로드 및 결합 함수
def load_and_concatenate_npy_files(file_list):
    data_list = []
    for file in file_list:
        data = np.load(file)
        data_list.append(data)
    return np.concatenate(data_list, axis=0)

# 모든 npy 파일을 하나의 큰 배열로 합치기
X_train_apt = load_and_concatenate_npy_files(X_train_files)
X_test_apt = load_and_concatenate_npy_files(X_test_files)
y_train_apt = load_and_concatenate_npy_files(y_train_files)
y_test_apt = load_and_concatenate_npy_files(y_test_files)

# 데이터 형태 확인
print(f"X_train_apt shape: {X_train_apt.shape}")
print(f"X_test_apt shape: {X_test_apt.shape}")
print(f"y_train_apt shape: {y_train_apt.shape}")
print(f"y_test_apt shape: {y_test_apt.shape}")

output_dir = r'C:\수어 데이터셋\output_frames\merged_data'

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 합쳐진 배열을 npy 파일로 저장
np.save(os.path.join(output_dir, 'X_train_apt_merged.npy'), X_train_apt)
np.save(os.path.join(output_dir, 'X_test_apt_merged.npy'), X_test_apt)
np.save(os.path.join(output_dir, 'y_train_apt_merged.npy'), y_train_apt)
np.save(os.path.join(output_dir, 'y_test_apt_merged.npy'), y_test_apt)

print("Merged files have been saved successfully.")
