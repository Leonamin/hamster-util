import pandas as pd

# CSV 파일 읽기
input_file = 'input.csv'  # 원본 CSV 파일명
output_file = 'output.csv'  # 중복을 제거한 결과를 저장할 CSV 파일명

# 데이터 불러오기
data = pd.read_csv(input_file, header=None)

# 첫 번째 열의 중복을 기준으로 중복된 행 제거 (첫 번째 발생한 중복만 유지)
data_unique = data.drop_duplicates(subset=[0])

# 결과를 새로운 CSV 파일로 저장
data_unique.to_csv(output_file, index=False, header=False)

print(f"{len(data_unique)}개의 중복되지 않은 행이 {output_file}에 저장되었습니다.")
