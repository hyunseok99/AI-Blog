# 1. slim 이미지를 베이스로 사용 (유지)
FROM python:3.11-slim

# 2. 필수 시스템 패키지 한 번에 설치 (빌드 속도 개선)
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# 3. Bun 설치
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

# 4. mdflow 설치 (npm 대신 bun을 사용하면 더 빠릅니다)
RUN bun install -g mdflow

# 5. gemini cli 설치
RUN npm install -g @google/gemini-cli

# 6. 작업 디렉토리 설정
WORKDIR /app
RUN echo $PATH
# 7. 의존성
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 8. 코드 복사
COPY . .

# 9. 권한 및 환경 설정
RUN mkdir -p /app/output
ENV PYTHONUNBUFFERED=1

# 10. 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]