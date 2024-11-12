import csv
import re
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from dotenv import load_dotenv
import os
import json


# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# txt 파일에서 instruction 로드
with open("instruction.txt", "r", encoding="utf-8") as file:
    instruction = file.read()
    if instruction == "":
        exit("Instruction이 비어있습니다. instruction.txt 파일을 확인해주세요.")

# json 파일에서 input , output 파일 이름 로드
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    input_file_name = config.get("input_file_name")
    output_file_name = config.get("output_file_name")
    if input_file_name == "":
        exit("input_file_name 이 비어있습니다. config.json 파일을 확인해주세요.")
    if output_file_name == "":
        f'{input_file_name.split(".")[0]}_output.csv'


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
    input_file_path = os.path.join('input', input_file_name)
    output_file_path = os.path.join('output', output_file_name)

    try:
        with open(input_file_path, mode='r', encoding='utf-8') as input_file, \
                open(output_file_path, mode='w', encoding='utf-8', newline='') as output_file:
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
                # summary = summarize_transcript(full_transcript)
                # print("Summary: " + summary)
                # if summary is not None:
                #     row[3] = summary
                # else:
                #     row[3] = "요약 실패"

                # 결과 파일에 쓰기
                writer.writerow(row)

    except Exception as e:
        print(f"An error occurred: {e}")
