<div align="center">
<h2> ⭐ 2024 1st Semester OpenSourceProgramming Team Project 🍀</h2>
Sign Language(수어) 앞의 두 철자인 S, L을 따서 대한민국의 수도이자 전 세계적으로 유명한 도시인 서울을 떠올릴 수 있도록 SeouL이라는 이름을 붙였습니다.
"SeouL"에는 많은 사람들이 사용하기에 편리하고, 간단하여 우리나라 수도인 서울과 같이 긍정적인 평판을 가진 프로그램이 되기를 바라는 큰 포부를 담고 있습니다. 이 프로그램은 사회적 가치를 지니며 많은 이들에게 유익한 도구가 되기를 목표로 하고 있습니다.🍀
</div>

## 목차
  - [개요](#개요) 
  - [팀원&역할분담](#팀원&역할분담)
  - [Project 구조](#Project-구조)
  - [Requirements](#Requirements)
  - [Help](#Help)
  - [SeouL 데모](#SeouL-데모)

## 개요
- 프로젝트 이름: 모두를 위한 실시간 수어-텍스트 변환 통역 서비스(SeouL) 🚌
- 프로젝트 지속기간: 2024.05-2024.06
- 팀 이름: 수어 업고 튀어
- 👪 팀원&역할분담
>   |박다은|**팀장**, UI 개발, UI 연결|
>
>  |박윤서|UI 디자인, UI 연결|
>
>  |정채리|인공지능 모델|
>
>  |한은정|mediapipe&웹캠구성|

***

## Project 구조

```
├── cam
│   ├── face+body+2hands
│   └── only 2hands(blue, yellow)
├── data
│   ├── hospital.avi 또는 .mp4
│   ├── pharmacy.avi 또는 .mp4
│   ├── apt.avi 또는 .mp4
│   ├── school.avi 또는 .mp4
│   └── kindergarten.avi 또는 .mp4
├── model
|   ├── learn.py
|   ├── my_lstm_model_15.h5
│   └── my_lstm_model.h5
├── result
|   ├── UI_result.zip
|   └── cam_result.mp4
├── 전처리
│   ├── changecsv.py
│   ├── csvmerged.py
│   └── processed
├── final.py
└── UI
    ├── index.html 
    ├── styles.css
    ├── scripts.js
    └── sign_proj
        └── app
            ├── static
            |   ├── figma first page.png
            |   ├── styles.css
            |   └── scripts.js
            ├── templates
            |   ├── about.html
            |   ├── index.html
            |   └── sign_language.html
            ├── main.py
            ├── my_lstm_model_15.h5
            └── my_lstm_model.h5
```

## Requirements
* Anaconda 가상환경 활성화
  * Install google mediapipe:
    ```shell
    pip install mediapipe opencv-python
    ```
  * python version = 3.9
  * Install 'flask' for UI:
    ```shell
    pip install flask
    ```

* SeouL/UI/sign_proj/app의 모든 파일을 한 공간 안에 다운로드해야 합니다.
* templates 폴더 안의 소스코드들은 한 폴더에 따로 묶어둬야 합니다.

* Anaconda 에서 main.py를 실행시킵니다.
    ```shell
    python main.py
    ```

* 메세지가 뜨면 url을 입력할 수 있는 인터넷을 연결합니다.
    ```shell
    Serving Flask app 'main'
    ...(생략)
    ```

## Help

>![Google Mediapipe](https://github.com/onesilver04/SeouL/assets/141193305/bb47481d-3ddf-43c0-905b-2a710dcf3e23)
>
>저희 팀은 Google의 MediaPipe라는 비전 AI 오픈 소스 프레임워크를 사용했습니다.
(실시간 비주얼 컴퓨팅 처리 및 해석에 매우 용이)

길을 물어보거나 방향 등을 농인분들이 설명하기 쉬우려면 큰 건물들이 주로 사용될 것을 예상하고
(병원, 약국, 아파트, 학교, 유치원) 총 5가지의 수화에 대해 학습시켰습니다.

# SeouL 데모

lstm + mediapipe 연결 영상 & UI까지 연결한 최종 완성본 영상
여기에-->[ move to the file] (https://github.com/onesilver04/SeouL/tree/main/result)
