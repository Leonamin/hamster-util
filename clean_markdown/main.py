import csv
import re

# 마크다운 문법을 제거하는 함수


def remove_markdown(text):
    # 제목(##), 인라인 코드(``) 등 마크다운 패턴 정의
    markdown_patterns = [
        r'`[^`]+`',        # 인라인 코드
        r'#+ ',            # 제목
        r'\*\*[^*]+\*\*',  # 굵은 텍스트
        r'\*[^*]+\*',      # 기울임 텍스트
        r'\[.*?\]\(.*?\)',  # 링크 텍스트
    ]
    # 각 패턴을 순회하면서 일치하는 모든 부분을 공백으로 대체
    for pattern in markdown_patterns:
        text = re.sub(pattern, '', text)
    return text.strip()

# CSV 파일 읽고 마크다운 문법 제거하여 새 파일에 저장


def clean_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
            open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 각 셀의 마크다운을 제거하고 저장
        for row in reader:
            cleaned_row = [remove_markdown(cell) for cell in row]
            writer.writerow(cleaned_row)


# 파일 경로에 따라 입력 및 출력 파일 이름을 설정하세요.
input_file = 'youtube_link_short.csv'
output_file = 'youtube_link_short_cleaned.csv'
clean_csv(input_file, output_file)
