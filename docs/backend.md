# Modu Math 백엔드

기존 Django 웹 편집기에 Django REST Framework 기반 학습 API를 추가했다. 원본
`semantic.json`, `solvable*.json`, `layout.json`, `renderer.json` 파일과 DSL 빌드
파이프라인은 그대로 유지하며, 관리 명령이 JSON 문서를 PostgreSQL/SQLite의
`Problem` 레코드로 복사한다.

## 데이터 모델

- `Problem`: `(problem_id, language)`가 유일하다. 언어·학년·문제 유형은 목록
  검색용 컬럼이고, concepts/skills/answer 및 네 종류의 원본 JSON 문서를 JSONField로
  보관한다.
- `Attempt`: 인증 사용자와 문제, 제출 답안, 서버 판정 결과, 풀이 시간(ms), 힌트 및
  재시도 횟수, 이벤트 배열을 기록한다. 클라이언트가 보낸 `is_correct` 값은 무시한다.
- `Mastery`: 사용자와 개념의 조합별 누적 시도/정답 수 및 `정답 수 / 시도 수` 점수를
  저장한다. 새 Attempt가 저장될 때 해당 문제의 모든 concepts가 한 트랜잭션에서
  갱신된다.

문제 카탈로그와 사용자별 최근 기록 조회에 복합 인덱스를 두었다. 목록 API는 큰 JSON
본문을 제외하고 페이지당 50개를 반환하므로 문제 수가 11,000개 이상이어도 전체
문서를 매번 직렬화하지 않는다.

## 로컬 실행(SQLite)

Python 3.10 이상과 `uv` 사용을 권장한다.

```bash
uv sync --extra dev
uv run python manage.py migrate
uv run python manage.py sync_problems
uv run python manage.py runserver
```

`DATABASE_URL`이 없으면 저장소 루트의 `db.sqlite3`를 사용한다. 이 파일과 WAL/저널
파일은 `.gitignore`에 포함되어 Git으로 관리되지 않는다.

## Docker Compose 실행(PostgreSQL)

```bash
docker compose up --build -d
docker compose exec web python manage.py sync_problems
docker compose logs -f web
```

API와 기존 편집기는 각각 `http://localhost:8000/api/v1/`,
`http://localhost:8000/editor-konva/`에서 접근한다. 데이터베이스 볼륨까지 제거할 때만
`docker compose down -v`를 사용한다.

직접 PostgreSQL을 사용할 때는 `.env.example`을 `.env`로 복사하고 연결 정보를
수정한다. Django는 다음 형태의 환경변수를 읽는다.

```dotenv
DATABASE_URL=postgresql://modu_math:password@localhost:5432/modu_math
```

운영 환경에서는 반드시 `MODU_MATH_WEB_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`,
`DJANGO_DEBUG=false`를 별도로 설정한다.

## 문제 동기화

```bash
uv run python manage.py sync_problems
uv run python manage.py sync_problems --dry-run
uv run python manage.py sync_problems --root C:/data/problems
```

명령은 언어 디렉터리의 `*.semantic.json`을 기준으로 동명의 최신
`*.solvable*.json`, `.layout.json`, `.renderer.json`을 읽는다. 같은 자연 키가 있으면
update하고 없으면 create하므로 반복 실행할 수 있다. concepts는 semantic metadata의
concepts/tags와 manifest의 domain/unit/topic에서, skills는 metadata와 solvable의
method에서 채운다. 원본 파일에는 쓰지 않으며 DB에서 사라진 파일을 자동 삭제하지도
않는다.

## 인증과 API

모든 응답은 JSON이다. 문제 읽기는 공개이고 풀이 및 숙련도는 토큰이 필요하다.

| Method | 주소 | 설명 |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register/` | 회원가입 및 토큰 발급 |
| `POST` | `/api/v1/auth/login/` | 로그인 및 토큰 발급 |
| `GET` | `/api/v1/problems/` | 문제 목록 |
| `GET` | `/api/v1/problems/{db_id}/` | 문제와 기존 JSON 상세 |
| `POST` | `/api/v1/attempts/` | 풀이 제출, 서버 채점 및 숙련도 갱신 |
| `GET` | `/api/v1/attempts/`, `/api/v1/attempts/{id}/` | 로그인 사용자의 풀이 기록 |
| `GET` | `/api/v1/masteries/` | 로그인 사용자의 개념별 숙련도 |

문제 목록은 `language`, `grade`, `problem_type` 쿼리 파라미터와 DRF의 `page`
파라미터를 지원한다. 풀이 목록은 `problem_id`로 필터링할 수 있다.

### 회원가입과 로그인

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","email":"student@example.com","password":"strong-pass-123"}'

curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"strong-pass-123"}'
```

응답의 `token`을 Flutter를 포함한 클라이언트에서 다음처럼 전송한다.

```http
Authorization: Token <token>
```

### 문제 조회와 풀이 제출

```bash
curl "http://localhost:8000/api/v1/problems/?language=ko&grade=3&page=1"

curl -X POST http://localhost:8000/api/v1/attempts/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": 1,
    "submitted_answer": {"choice_id": "choice.3"},
    "elapsed_ms": 8200,
    "hint_count": 1,
    "retry_count": 0,
    "events": [{"type": "answer_submitted", "at_ms": 8200}]
  }'
```

`problem`은 목록 응답의 숫자형 DB `id`이다. `submitted_answer`는 JSON 값으로 숫자,
문자열, 선택지 ID 객체 등을 받을 수 있다. 서버는 저장된 `answer.value`와
`answer.answer_key`를 기준으로 판정하며 `is_correct`는 읽기 전용이다.

```bash
curl -H "Authorization: Token <token>" http://localhost:8000/api/v1/attempts/
curl -H "Authorization: Token <token>" http://localhost:8000/api/v1/masteries/
```

## 검증

```bash
uv run python manage.py makemigrations --check
uv run python manage.py check
uv run pytest
```
