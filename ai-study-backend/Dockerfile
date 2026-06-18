# study-backend
FROM python:3.11-slim

# mdflow 가동을 위해 Node.js 및 npm 설치 후 글로벌 설치
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g mdflow

# 1. dir 설정
WORKDIR /app

# 2. package 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3. backend 코드 복사
COPY . /app

# 4. 보안 샌드박스 및 마운트용 디렉토리 미리 선언 (권한 꼬임 방지)
RUN mkdir -p /app/output

# 5. 환경 변수 설정 (로그 실시간 출력을 위해 버퍼링 해제)
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]