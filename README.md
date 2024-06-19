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
│   ├── hospital.avi
│   ├── pharmacy.avi
│   ├── apt.avi
│   ├── school.avi
│   └── kindergarten.avi
├── model
|   ├── learn.py
|   ├── my_lstm_model15.h5
│   └── my_lstm_model.h5
├── 전처리
때
