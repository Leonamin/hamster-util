
## 환경 설정
### .env 설정하기
.env를 만들어 **OPENAI_API_KEY**를 넣어줍니다

```
OPENAI_API_KEY=sk-proj-wallahwallahwallahwallahwallahwallahwallahwallahwallahwallahwallahwallah
```

### instruction.txt 설정하기
본인이 원하는 형식을 설정해 줍니다.

### config.json 설정하기
`input_file_name`과 `output_file_name`을 설정해줍니다. 파일 이름은 확장자까지 작성해줍니다.
`input_file_name`은 필수 입력이며 `output_file_name`은 input이 없을 경우 `input_file_name` 뒤에 _output이 추가로 붙습니다

### 파일 제공하기
input 폴더를 생성하여 input 폴더 하위에 `input_file_name`으로 설정한 파일을 저장합니다.