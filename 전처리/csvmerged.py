import pandas as pd
import glob
from sklearn.preprocessing import MinMaxScaler
# school 단어의 CSV 파일들을 모두 불러와서 하나의 데이터프레임으로 통합
file_paths = glob.glob('hand_landmarks/school_*.csv')  # school로 시작하는 모든 CSV 파일 경로
dfs = [pd.read_csv(file) for file in file_paths]
school_df = pd.concat(dfs, ignore_index=True)

# 데이터프레임의 수어 손 벡터 열을 정규화
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(school_df.iloc[:, 1:])  # 첫 번째 열은 프레임 번호 등의 메타 데이터일 수 있음

# 정규화된 데이터로 데이터프레임 업데이트
school_df.iloc[:, 1:] = scaled_data

# 정규화된 데이터프레임을 CSV 파일로 저장
school_df.to_csv('processed_output/normalized_school_data.csv', index=False)
