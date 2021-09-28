# ai-study


1단계 : 앱으로 학습방에 참여하여 자신의 학습몰입도 측정

- AI학습 상태 기록 (start, stop, empty)
- 학습방 생성 (관리자)
- 학습방 참여
- 개인별 학습도 Report 제공

2단계 : 학습목표 설정 (각종 시험), 목표일자까지 일정관리, 기간별 학습 몰입도 측정

Architecture : MLOps
- App + 기계학습/딥러닝 (Tensorflow.js)
- webRTC
- Python web / MariaDB


----------------------------

# 실행 방법1
1. python 가상환경 설치
2. pip install mysqlclient 설치
3. requirements.txt 설치
    - pip install -r requirements.txt
4. python manage.py runserver


# 실행 방법2
1. python 가상환경 설치
2. mysqlclient wheel 파일 설치
    - https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
    - pip install [생성된 .whl파일]
4. pip install mysqlclient 설치
5. requirements.txt 설치
    - pip install -r requirements.txt

6. python manage.py runserver


