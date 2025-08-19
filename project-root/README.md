# Allcode Backend (FastAPI on Render)

## 로컬 실행
1) Python 3.11+
2) `cp .env.example .env` 후 값 채우기
3) `pip install -r requirements.txt`
4) `uvicorn app.main:app --reload`

## 환경변수 (.env)
- JWT_SECRET=초강력랜덤문자열
- DATABASE_URL=postgresql+psycopg2://USER:PASS@HOST:5432/DBNAME
- ALLOWED_ORIGINS=*

## Render 배포
- New → Web Service → GitHub 연결
- rootDir: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Managed Postgres 생성 후 DATABASE_URL 연결
- `/health/z` 로 헬스체크
