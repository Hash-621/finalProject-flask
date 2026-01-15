# flask_server/Dockerfile

# 1. 가벼운 파이썬 이미지 사용
FROM python:3.9-slim

# 2. 작업 폴더 설정
WORKDIR /app

# 3. 라이브러리 목록 복사 및 설치
# (캐싱 효과를 위해 소스 복사 전에 수행)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 전체 복사
COPY . .

# 5. Flask 기본 포트 노출
EXPOSE 5000

# 6. 실행 명령어 (app.py 실행)
CMD ["python", "mat_server.py"] 