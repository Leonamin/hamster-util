import csv
import re
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

instruction = """
주어진 영상들은 만성질환관리(고혈압, 당뇨병) 환자분들께 전달될 일상생활습관 개선, 운동, 식습관 관련 영상들의 자막 텍스트야.
아래의 조건에 맞게 내용을 요약해줘.
조건: 핵심 정보만 남기기: 건강 주제와 관련이 없는 내용은 모두 제외해줘.
- 오탈자 및 띄어쓰기 수정: 문법적 오류나 오탈자는 모두 올바르게 수정하고, 자연스럽고 매끄러운 문장으로 고쳐줘.
- 쉬운 표현 사용: 어려운 용어나 기술적인 표현은 피하고, 어르신들이 쉽게 이해하실 수 있는 일상적인 말로 바꿔줘.
- 군더더기 제거: 처음 시작이 안녕하세요, 어르신 이런 부가적인 인사로 시작하는 부분은 제외해줘
- 길이는 꼭 150자 이내로 마크다운이 아닌 평문으로 넷플릭스 영상 소개 같은 느낌으로 정보를 요약해서 전달해줘.
텍스트:

"""

# 나머지 함수들 (is_correct_url, extract_video_id 등)은 그대로 유지


def is_correct_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})(?=\?|&|$)", url)
    if match:
        return match.group(1)
    return None


def get_full_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['ko'])
        full_transcript = " ".join([t['text'] for t in transcript_list])
        return full_transcript
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def summarize_transcript(transcript):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": transcript}
            ],
            model="gpt-4o-mini",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"An error occurred with GPT summarization: {e}")
        return None


if __name__ == "__main__":
    input_file_name = 'youtube_links.csv'
    output_file_name = f'{input_file_name.split(".")[0]}_output.csv'

    try:
        with open(input_file_name, mode='r', encoding='utf-8') as input_file, \
                open(output_file_name, mode='w', encoding='utf-8', newline='') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            for row in reader:
                value = row[0]
                while len(row) < 4:
                    row.append("")

                if value == "":
                    continue

                if not is_correct_url(value):
                    continue

                video_id = extract_video_id(value)
                print(f"Video Id: {video_id}")

                if video_id is None:
                    writer.writerow(row)
                    continue

                row[1] = video_id

                full_transcript = get_full_transcript(video_id)

                if full_transcript is None:
                    writer.writerow(row)
                    continue

                # print("Full Transcript: " + full_transcript)
                row[2] = full_transcript

                # GPT 요약 추가
                summary = summarize_transcript(full_transcript)
                print("Summary: " + summary)
                if summary is not None:
                    row[3] = summary
                else:
                    row[3] = "요약 실패"

                # 결과 파일에 쓰기
                writer.writerow(row)

    except Exception as e:
        print(f"An error occurred: {e}")
