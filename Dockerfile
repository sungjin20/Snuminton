# Python 베이스 이미지
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 코드 복사
RUN rm -rf /app/*
COPY . /app

# Copy service account key to the container
#COPY sodium-diode-445205-v1-a62e0cedcb8d.json /app/

# 필요한 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# Flask 앱 실행
CMD ["python", "app.py"]