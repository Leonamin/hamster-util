import pandas as pd
import json

# 입력 파일 경로와 출력 파일 경로
input_file_path = "input.json"  # JSON 파일 경로
output_file_path = "output.csv"  # CSV 파일 경로

# JSON 파일 읽기
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# DataFrame 생성
df = pd.DataFrame(data)

# CSV 파일로 저장
df.to_csv(output_file_path, index=False, encoding="utf-8-sig")

print(f"CSV 파일이 생성되었습니다: {output_file_path}")
