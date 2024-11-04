import json
import csv


def load_languages(file_path='languages.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        languages_list = json.load(file)

    # 리스트 형식인 경우 평탄화하여 key-value 형태로 변환
    languages = {}
    for lang_dict in languages_list:
        languages.update(lang_dict)

    return languages


def choose_mode():
    mode = input(
        "1: .arb를 .csv로 바꾸기\n2: .csv를 .arb로 바꾸기\n모드 선택 (1/2): ")
    return int(mode)


def configure_languages(languages):
    active_languages = {key: True for key in languages}
    while True:
        print("\n".join([f"{lang}({i + 1}): [{'o' if active else 'x'}]"
                        for i, (lang, active) in enumerate(active_languages.items())]))
        choice = input("숫자를 입력해서 언어 활성화 (0을 입력하면 시작): ")

        if choice == "0" or choice == "":
            break
        else:
            idx = int(choice) - 1
            key = list(active_languages.keys())[idx]
            active_languages[key] = not active_languages[key]
    return {k: v for k, v in active_languages.items() if v}


def arb_to_csv(languages, active_languages, input_folder='input', output_file='output/translations.csv'):
    data = {}
    headers = ['label / lang'] + list(active_languages.keys())

    for lang, arb_file in languages.items():
        if lang in active_languages:
            with open(f"{input_folder}/{arb_file}", 'r', encoding='utf-8') as file:
                arb_data = json.load(file)
                for key, value in arb_data.items():
                    # Description keys도 CSV에 포함
                    if key not in data:
                        data[key] = {}
                    if isinstance(value, str):
                        data[key][lang] = value  # Raw string 저장
                    else:
                        data[key][lang] = json.dumps(value, ensure_ascii=False)

    # Save to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for label, translations in data.items():
            row = [label] + [translations.get(lang, '')
                             for lang in active_languages]
            writer.writerow(row)


def csv_to_arb(languages, active_languages, input_file='output/translations.csv', output_folder='output'):
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # 첫 번째 행을 건너뜀
        lang_indices = {headers[i]: i for i, lang in enumerate(
            headers) if lang in active_languages}

        data_by_lang = {lang: {} for lang in active_languages}
        for row in reader:
            label = row[0]
            for lang, idx in lang_indices.items():
                value = row[idx].strip()
                if value:
                    # JSON 객체인지 확인하고 파싱
                    try:
                        parsed_value = json.loads(value)
                        data_by_lang[lang][label] = parsed_value
                    except json.JSONDecodeError:
                        # 문자열인 경우 그대로 저장
                        data_by_lang[lang][label] = value

    # Write to ARB files
    for lang, arb_data in data_by_lang.items():
        with open(f"{output_folder}/{languages[lang]}", 'w', encoding='utf-8') as arb_file:
            json.dump(arb_data, arb_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    languages = load_languages()
    active_languages = configure_languages(languages)
    mode = choose_mode()

    if mode == 1:
        arb_to_csv(languages, active_languages)
        print("ARB를 CSV로 변경 완료.")
    elif mode == 2:
        csv_to_arb(languages, active_languages)
        print("CSV를 ARB로 변경 완료.")
