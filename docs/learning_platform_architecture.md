# 학습관리 플랫폼 전환

## Phase 0 — 실제 소스 분석 (2026-10-30)

저장소의 작업 시작 시점에 day_01/00469 및 day_02 문제 원본·파생물과 Flutter 정적 번들의 미커밋 변경이 있었다. 이 파일들은 이번 플랫폼 개발의 수정 대상에서 제외한다. DB를 초기화하거나 기존 데이터 마이그레이션을 되돌리지 않는다.

### 확인한 구현과 재사용 경계

| 영역 | 실제 구현 | 이번 확장 |
| --- | --- | --- |
| 문제 엔진 | `src/modu_math/dsl`, `pipeline`, `renderer`, `solvable` 및 `schema` | 계약과 생성 파이프라인 유지 |
| 저작 | `editor/services`의 DSL 저장·빌드·레이아웃 패치, `editor_next/src` React/Konva | 재사용, 관리 UI는 후속 단계 |
| 학습 DB | `learning/models.py`: Problem, ProblemTagging, Attempt, Mastery | 별도 관리 모델 추가, Attempt에 nullable 관계 추가 |
| 인증 | Django 기본 사용자, DRF TokenAuthentication, register/login | 기본 사용자 교체 없이 교사 그룹과 학생 프로필 추가 |
| 채점 | `Problem.check_answer`, `Attempt.save` 서버 채점·Mastery 갱신 | 배정된 문제는 고정된 정답·개념으로 채점 |
| 진단/추천 | `learning/services/diagnostics_service.py`, `recommendation_service.py` | 기존 개인 전체 통계 유지, 과제 통계 별도 계산 |
| 모바일 | `apps/mobile/lib/services`의 인증·문제 API·오프라인 Attempt, 기존 renderer 위젯 | 과제 API를 위한 별도 연동 필요 |
| 배포/DB | Django 설정에서 DATABASE_URL/PostgreSQL 및 로컬 SQLite 지원 | 두 DB에서 가능한 제약 사용 |

### 기존에 발견한 문제

1. 공개 Problem 상세 응답에 answer/semantic/solvable 원문이 포함된다. 과제 학생 응답은 별도 허용 목록으로 구성해야 한다.
2. `/api/editor/` Django 함수 뷰에는 인증 검사가 없다. 로컬 저작 도구를 그대로 인터넷에 공개하면 DSL 실행·원본 노출 위험이 있다. 운영 저작 API 보호 및 편집기 인증 연동이 필요하다.
3. 배포된 Flutter 정적 자산과 오프라인 번들 자체에 정답 원본이 포함된다. API를 보호해도 이 디렉터리를 공개하면 시험 보안을 제공할 수 없다. 운영 학생 번들과 저작/오프라인 번들을 분리해야 한다.
4. `answer_matches`는 여러 answer_key 중 하나만 맞아도 정답으로 처리할 수 있다. 다중 빈칸은 전체 정답을 비교하도록 보완하고 회귀 테스트한다.
5. Flutter의 기존 풀이 흐름은 로컬 정답·해설과 오프라인 채점을 전제로 한다. 과제는 전용 서버 채점 흐름이 필요하며 기존 일반 학습 흐름을 과제 제출로 오인하지 않아야 한다.

## Phase 1 설계

- 관리자: 기존 `is_staff`/`is_superuser`; 교사: 관리자가 부여한 `modu_teachers` 그룹. 회원가입 입력으로 권한을 부여하지 않는다.
- StudentProfile은 최소 사용자 정보만 참조한다. 생년월일·주소·보호자 정보는 수집하지 않는다.
- Classroom은 교사 소유, Enrollment는 학생별 pending/approved 관계다. 초대 코드 가입은 승인 대기이며 교사 승인이 필요하다.
- ProblemPublication은 원본 Problem과 분리한 상태·난이도 관리다. 기존 출판 정보가 없는 문제는 기존 공개 문제로 취급한다.
- ProblemSet/ProblemSetItem은 순서를 보존한다. Assignment 생성 시 AssignmentItem에 공개 콘텐츠, 정답, 개념을 복사한다. 원본·문제집 수정이 기존 과제에 영향을 주지 않는다.
- AssignmentRecipient는 배정 시점의 학생 명단이다. 이후 Enrollment 변경은 기존 배정에 영향을 주지 않는다.
- AssignmentProgress는 중간 저장, Attempt는 실제 채점 기록이다. 과제 문항·수신자 관계와 중복 제출 키, 시도 번호에 DB 제약을 둔다.
- 수신자 행 잠금과 트랜잭션으로 재시도 한도/중복 제출/최종 제출을 직렬화한다. PostgreSQL 운영에서 행 잠금을 사용한다. SQLite는 개발·테스트용이며 동시 쓰기 검증을 대체하지 않는다.
- 삭제는 기록 보존 우선(PROTECT), 기존 Attempt 관계는 nullable이며 기존 레코드를 수정하지 않는다. 과제 통계는 수신자의 해당 과제 최종 문항별 시도로 계산한다.
- 시작/마감은 서버 시각으로 검사한다. 정답 공개는 immediate/after_submission/after_due/never 정책이며 학생의 결과·정답·해설을 함께 제어한다.

## 단계별 진행 기록

Phase 0: 위 표와 기존 위험 분석 완료.

Phase 1: 백엔드의 배정→학생별 풀이→서버 채점→결과 조회→오답 재배정 흐름 구현. 자동 테스트에서 교사 1명·학생 2명·10문항을 실제 API로 검증했다. UI를 포함한 전체 플랫폼 완료를 의미하지 않는다.

Phase 2: `/teacher/` React 교사 관리 화면의 7개 메뉴, 실제 API 연동, 기존 Konva 편집기 인증/이동 연결 구현. 상세 내용은 아래 Phase 2 기록을 참고한다.

Phase 3 (예정): 기존 AuthService와 renderer를 이용한 Flutter 전용 과제 목록·중간 저장·서버 채점·최종 제출·복습 화면.

Phase 4 (예정): PostgreSQL 동시 제출 검증, 운영용 정적 번들 분리, 실제 웹→두 학생→교사 결과 흐름, 전체 회귀·Flutter 분석·React 타입/빌드.

## Phase 1 변경 파일 및 DB

- `learning/platform_models.py`: 관리 모델 10개. 요구 모델 7개에 문제 공개 상태, 배정 문항 스냅샷, 중간 저장 모델을 추가했다.
- `learning/models.py`: 기존 Attempt에 nullable `assignment_item`, `recipient`, `submission_key`, `assignment_try` 추가. 기존 Attempt/Mastery의 PK·필드·기록은 유지한다.
- `learning/migrations/0004_learning_platform.py`: 관리 테이블, FK, 순서/수신자/중복 요청/시도 번호의 유일 제약, 일정·시도 한도 검사, 조회 인덱스. FK 컬럼 생성 후 제약을 생성하도록 순서를 검증했다.
- `learning/platform_permissions.py`, `platform_serializers.py`, `platform_views.py`, `services/assignments.py`: 역할·소유권 검사, 입력 검증, 스냅샷 생성, 공개 정책과 과제 API.
- `learning/serializers.py`, `views.py`, `urls.py`: 기존 인증/API와 연결. 기존 URL을 제거하지 않는다. 공개 문제 상세에서 정답·풀이를 제외하는 것은 의도적인 보안 변경이다. 관리자/교사는 원문을 조회할 수 있다.
- `learning/services/diagnostics_service.py`, `recommendation_service.py`: 미공개 과제 채점 결과를 기존 API로 우회 조회하지 못하게 한다. 공개된 과제의 개념 진단은 스냅샷 개념을 사용한다. 추천은 공개 문제만 대상으로 한다.
- `learning/middleware.py`, `settings.py`: `DEBUG=False` 운영 저작 API에 교사/관리자 토큰을 요구한다. `DEBUG=True`는 신뢰할 수 있는 로컬 저작 환경에서만 사용한다.
- `learning/management/commands/set_teacher.py`: 신뢰된 서버 관리자가 교사 그룹 부여/회수. 사용자 권한 API도 관리자에게만 허용하며 일반 staff가 admin으로 승격시키지 못하게 한다.
- `sync_problems.py`: 새 수입 문제는 초안이며 `--new-status published`로 기존 공개 자료를 수입할 수 있다. 기존 검수 상태는 수입으로 덮어쓰지 않는다. 원본에서 누락된 Problem을 삭제하지 않는다.
- `tests/backend/test_learning_platform.py`, `test_platform_migration.py`: 권한·채점·스냅샷·수신자 보존·공개 정책·통계 분리·레거시 데이터 이행 검증.

기존 사용자는 필요 시 학급 가입 또는 관리자의 학생 역할 지정에서 StudentProfile을 생성한다. 기존 계정을 일괄 변경하지 않는다. 이메일은 선택 사항이며 교사 등록 학생은 아이디와 비밀번호만 받는다.

로컬 SQLite에는 백업 후 0004를 적용했다. 적용 전후 users=0, problems=387, attempts=0, masteries=0으로 동일했다. 기존 Attempt/Mastery가 있는 DB의 이행도 별도 테스트 DB에서 검증했다. 백업은 `.tmp/learning-platform-before-0004.sqlite3`, 개수 확인 기록은 `.tmp/learning-platform-migration-check.json`에 있다. 이 개인정보 포함 가능 파일들은 Git에 추가하지 않는다.

운영에서는 DB 백업 후 `python manage.py migrate --noinput`을 실행한다. 새 기록이 생긴 후 0003으로 되돌리면 신규 과제 데이터가 삭제되므로 운영 롤백은 테이블 삭제 대신 이전 앱 배포 또는 백업 복구 계획에 따라 수행한다. PostgreSQL에서 동시 요청을 실제 실행하는 검증은 미완료다.

## Phase 1 API 사용

모든 신규 관리·학생 API는 `Authorization: Token <token>`을 요구한다. 학생/학급 ID는 각각 StudentProfile/Classroom의 DB PK이며, 문항 응답의 `item_id`는 AssignmentItem의 PK다. 학생 과제 URL의 ID는 수신자 ID가 아닌 Assignment의 PK다.

| 메서드·경로 (`/api/v1/` 기준) | 용도 |
| --- | --- |
| POST `auth/register/`, `auth/login/` | 기존 인증. 가입에 선택적 `invite_code`, 응답에 `role` 추가 |
| GET `auth/me/`, POST `auth/logout/` | 현재 계정, 서버 토큰 폐기 |
| GET/PATCH `admin/users/{id}/` | 관리자의 역할·활성 상태 관리 (목록은 `admin/users/`) |
| GET/POST `students/`, GET `students/{id}/` | 담당 학생 목록·등록·조회 |
| GET/POST `classes/`, PATCH `classes/{id}/` | 담당 학급 관리·보관 |
| GET/POST `classes/{id}/enrollments/` | 가입 대기 포함 명단·담당 학생 편성 |
| PATCH `classes/{id}/enrollments/{id}/` | `status: pending/approved/inactive` |
| POST `classes/{id}/rotate-code/` | 초대 코드 재발급 |
| POST `student/join-class/` | `invite_code`로 승인 대기 가입 |
| GET `problems/` | 기존 검색 + `unit`, `concept`(정확한 개념 ID), `difficulty`(1~5), `status` |
| GET/PATCH `problems/{id}/publication/` | 교사/관리자의 공개 상태·난이도 관리 |
| GET/POST `problem-sets/`, GET/PUT/PATCH `problem-sets/{id}/` | 순서가 있는 문제집 |
| POST `problem-sets/{id}/duplicate/` | 문제집 복제 |
| GET/POST `assignments/`, GET/PATCH `assignments/{id}/` | 배정·상태 변경 |
| GET `assignments/{id}/recipients/`, `results/` | 수신자·문항·개념별 결과와 미제출 |
| POST `assignments/{id}/reassign-wrong/` | 제출 완료한 수신자의 오답 스냅샷 재배정 |
| GET `student/assignments/`, `student/assignments/{id}/` | 내 과제·이어 풀기·공개된 결과 |
| PUT `student/assignments/{id}/progress/` | 채점 없는 문항별 중간 저장 |
| POST `student/assignments/{id}/answers/` | 서버 채점과 중복 요청 키 적용 |
| POST `student/assignments/{id}/submit/` | 모든 문항 응답 후 최종 제출 (반복 호출 안전) |
| GET `teacher/dashboard/` | 담당 과제 범위의 집계 |

문제집 생성:

```json
{"title":"덧셈 10문항","problem_ids":[1,2,3,4,5,6,7,8,9,10]}
```

배정 (`max_attempts`는 최초 풀이를 포함한 문항별 총 시도 수, 1~20):

```json
{"title":"이번 주 과제","problem_set":1,"student_ids":[1,2],"class_ids":[],"max_attempts":2,"release_policy":"after_submission","starts_at":null,"due_at":null}
```

문항 답안 제출 (`submission_key`는 클라이언트가 생성해 재전송 시 유지, 예: UUID):

```json
{"item_id":1,"answer":507,"submission_key":"6fdb2ed7-02fc-4c2c-ae96-b9895c4f99b1","elapsed_ms":1200,"hint_count":1}
```

`elapsed_ms`는 이번 시도의 소요 시간이다. 시간·힌트 수는 클라이언트 보고 값이며 정답 판정에는 사용하지 않는다. 미공개 정책에서는 응답에 `is_correct`가 없다. 최종 제출은 빈 객체를 POST한다. 중간 저장은 `item_id`, `answer`만 PUT한다. 오답 재배정은 `recipient_id`, 선택적인 `title`을 POST한다.

과제 집계는 각 수신자·문항의 마지막 채점 시도를 기준으로 하고, 완료율은 답안을 채점한 문항 수/전체 문항 수다. 최종 제출 여부는 별도로 제공한다. 정답률의 분모는 전체 배정 문항 수이므로 미응답은 정답에 포함되지 않는다. 개인 진단/숙련도 API는 전체 공개된 학습 기록을 기준으로 하며 과제 집계와 합치지 않는다.

기존 공개 자료 일괄 수입: `python manage.py sync_problems --new-status published`. 새 자료 검수 수입: `python manage.py sync_problems`. 등록한 계정에 교사 권한 부여: `python manage.py set_teacher <username>` (회수는 `--revoke`). 관리자 생성에는 기존 Django `createsuperuser`를 사용한다.

## 기존 문제 보완과 한계

- **기존 문제 수정:** 다중 빈칸 일부 정답을 전체 정답으로 판정하던 비교 로직, 원본 누락 시 Problem/학습 기록을 삭제하던 수입 로직, 공개 상세·자산 API의 정답 원본 노출, 운영 저작 API 무인증 접근을 보완했다.
- **기존 회귀 실패 수정:** 최초 전체 실행에서 387개 통과/4개 실패. HEAD에도 존재하던 `tools/validate_generated_dsl.py::_run_build`의 필수 `emit_svg` 인자와 기존 호출부가 불일치했다. 기본값 `False`를 추가해 선택적 SVG 생성 계약과 기존 호출을 호환시켰다.
- **신규 구현:** 관리 테이블·API·권한·스냅샷·중복 제출·진행/결과 집계·이행 테스트.
- **Phase 1 이후 작업:** 교사 React 화면 및 운영 편집기 인증 연결은 Phase 2에서 구현했다. Flutter 과제 전용 화면·테스트, 학생용 배포에서 저작·오프라인 원본 번들 분리, PostgreSQL 동시 제출 테스트는 여전히 남아 있다.
- 공개 상세에서 정답을 제거했으므로 기존 Flutter의 로컬 채점/해설 흐름에는 과제용 API 연동이 필요하다. 기존 로컬 오프라인 자료와 저작 엔진의 파일 계약은 유지한다.
- 과제 관리 목록과 결과의 쿼리 수/페이지 처리는 학급 규모 이상의 대규모 운영 전에 최적화가 필요하다. 과제 문항은 최대 200개로 제한한다.

## 검증 기록

- 신규 플랫폼·이행 테스트: 초기 27개 통과, 이후 비파괴 수입 및 한글 개념 검색 테스트 각각 추가·통과 (현재 총 29개).
- 기존 backend 테스트: 16개 통과.
- Django system check 통과, `makemigrations --check --dry-run` 변경 없음.
- SQLite 이행 적용 및 기존 데이터 개수 보존 확인 완료.
- 전체 Python 회귀: **392개 통과, 48.35초**. 이후 한글 개념 검색 검증 1개를 추가하고 문제은행 권한 검증과 함께 **2개 통과**했다. PostgreSQL에서는 JSON 배열 포함 검색을 사용하고, SQLite에서는 정확한 태그 비교로 한글 검색을 보장한다.
- Phase 2/3 소스는 수정하지 않아 이번 단계에서 React/Flutter 검증을 완료했다고 보고하지 않는다. 후속 구현에서는 위 API 계약을 우선 사용하고, 일반 오프라인 풀이와 과제 제출의 저장 경로를 분리해야 한다.

## Phase 2 — 교사·관리자 웹 (2026-10-30)

### 구현한 기능

진입점은 Django의 **`/teacher/`** 이다. 기존 `/`와 `/editor-konva/` 경로는 유지한다. 기존에 부여된 교사/관리자 계정으로 로그인하며 학생 계정은 교사 화면 진입을 허용하지 않는다.

1. **대시보드:** 담당 학생·운영 학급·배정 과제·미제출 수, 최근 과제, 학습 준비 동선. 수치는 실제 API에서 읽는다.
2. **문제은행:** 학년·단원·개념·유형·언어·난이도·공개 상태 검색, 페이지 이동, 검색 중 선택 유지, 읽기 전용 Konva 미리보기, 정답 검수, 상태/난이도 저장, 원본 편집기 이동.
3. **문제집 관리:** 선택 순서로 생성, 문항 순서 이동/제거, 선택한 문제 추가, 제목·설명 수정, 복제. 저장 직후 배정 화면으로 이어진다. 기존 과제는 원본 문제집 수정과 독립적이다.
4. **과제 배정:** 학생 복수 선택 및 학급 배정, 한국 시간 기준 시작/마감, 문항별 총 시도 횟수, 정답·해설 공개 시점, 과제 상태 변경.
5. **학생 관리:** 최소 정보로 계정 등록, 담당 학생 목록. 관리자는 별도로 전체 계정의 역할·활성 상태를 관리한다. 권한 변경의 최종 판단은 서버에서 한다.
6. **학급 관리:** 생성, 보관/재운영, 초대 코드 복사/재발급, 학생 편성, 가입 대기 승인/비활성화.
7. **학습 결과:** 선택 과제의 학생별 완료율·정답률·시간·힌트·제출 상태, 문항/개념별 정답률, 문항별 답안·해설, 제출한 학생의 오답 재배정. 선택 과제는 URL `#results/{id}`에 보존되어 새 과제 생성·새로고침 때 바뀌지 않는다.

빈 목록·로딩·서버 오류·중복 클릭 방지·세션 만료를 처리한다. 입력 레이블은 각 컨트롤에 명시적으로 연결하고 모달은 브라우저 dialog의 초점 관리와 Escape 닫기를 사용한다. PC와 390px 너비에서 표시를 확인했다.

### 구조 및 변경 파일

- `editor_next/src/teacher/`: 독립 진입점, API/타입, 공통 컴포넌트, 문제은행, 학생/학급, 결과, 문제집/배정 폼, 스타일. UI와 API 호출을 분리한다.
- `editor_next/src/auth/session.ts`: 교사 토큰을 탭의 sessionStorage에 저장한다. URL·로그·문제 데이터에 토큰을 넣지 않는다.
- `editor_next/teacher.html`, `vite.config.ts`, Django `templates/editor_next/teacher.html`, `views.py`, 최상위 `urls.py`: 기존 편집기와 같은 Vite 프로젝트의 다중 진입점으로 빌드한다. 기존 편집기 출력 이름은 유지하고 공통 React/Konva 모듈을 공유한다.
- `editor_next/src/App.tsx`, `api/editorApi.ts`, `konva_editor/EditorKonva.tsx`: 운영 교사 권한 확인, API 토큰 헤더, `?problem=ko/day_XX/문제.dsl.py`로 원본 열기, 관리 화면 복귀.
- `learning/platform_views.py`, `middleware.py`, `urls.py`: `POST /api/v1/auth/editor-session/` 추가. 인증한 교사에게만 1시간 유효한 서명·HttpOnly·SameSite=Strict 이미지 쿠키를 발급한다. 운영에서는 Secure다. 쿠키의 인증 대체는 `/api/editor/assets/`의 GET/HEAD만 허용하며 저작 API JSON 조회/쓰기는 토큰 헤더를 계속 요구한다. 역할 회수·계정 비활성·토큰 삭제 시 이미지 접근도 차단되고 로그아웃 시 쿠키를 지운다.
- `learning/serializers.py`, `views.py`: 문제 목록에 `publication_status`/`difficulty` 추가, 최대 200개 `ids` 필터 지원, 공개 상태 관계를 함께 조회한다. 기존 학생 공개 문제 필터를 우회하지 않는다.
- `scripts/teacher-api.test.mjs`, `teacher-browser.test.mjs`, `tests/backend/test_teacher_workspace.py`, `seed_teacher_browser.py`: API 클라이언트·교사 웹·운영 인증 자동 검증. 브라우저 검증에 Playwright 개발 의존성 추가.

**DB 변경:** 이 단계에는 새 모델·마이그레이션이 없다. 개발 DB에 테스트 사용자·과제를 넣지 않았다. 브라우저 픽스처는 임시 디렉터리의 SQLite에만 생성하도록 경로를 검사한다.

### 검증

- TypeScript `npm run typecheck`, Vite `npm run build` 통과.
- 전체 Python 회귀 **398개 통과 (74.07초)**. 새 5개 검증은 교사 HTML 진입점, 목록/ID 검색 권한, 서명 이미지 쿠키 범위와 역할/토큰 회수, 학생 발급 차단, 로그아웃 쿠키 폐기다.
- API 클라이언트 새 6개 테스트 통과: 인증된 쓰기, 전체 페이지 수집/취소, 외부 URL로 토큰 전송 방지, 401 폐기, 읽기 쉬운 검증 오류, 편집기 경로 보존.
- 기존 편집기·API 클라이언트 Node 회귀 **47개 전체 통과 (12.88초)**. 텍스트 앵커, 정답 검수, 배치 동기화, 아바타 색상/교체 및 저장 후 재로딩을 포함한다.
- 실제 Chrome 브라우저 통합 검증 통과 (13.56초): 학생 계정의 교사 로그인 거부 → 교사 로그인/새로고침 유지 → 검색 중 10문항 선택 유지 → 순서 변경/문제집 생성 → 두 학생 배정 → 두 학생의 로그인·채점·최종 제출 **REST 요청** → 교사 화면 정답률 90% 확인 → 상세 오답/재배정 → 학생 등록 → 학급 편성/초대 가입 승인 → 운영 편집기 원본 열기 → 관리 화면 복귀 → 390px 화면 → 로그아웃. 이는 Flutter UI 검증을 대체하지 않는다.
- Django check 통과, 마이그레이션 드리프트 없음.
- 화면 캡처: `.tmp/teacher-browser/dashboard.png`, `results.png`, `mobile.png`. 테스트 산출물은 Git에서 제외한다.

**기존 문제 보완:** 아바타 교체 회귀 테스트 두 파일이 이동/수정된 실제 수업 예제(`S3_elem_3_008728`)에 의존해 실패했다. 문제 원본을 되돌리지 않고 `scripts/fixtures/legacy-avatar-layout.mjs`에 고정된 과거 도형을 분리했다. 기존 교체·다른 사람/이름/말풍선 보존·저장 후 재로딩 검증은 유지한다.

**남은 작업:** Phase 3 Flutter 학생 과제 전용 흐름과 Phase 4 배포/동시성 검증. 정답을 포함한 기존 오프라인/편집기 자산을 학생 운영 번들과 분리해야 한다. 이미지가 포함된 과제는 JSON 스냅샷뿐 아니라 이미지 파일의 접근·버전 보존도 확인해야 한다. Vite 빌드에는 기존 Konva 공통 모듈의 500kB 초과 경고가 남아 있으며 기능 검사 실패는 아니다.

브라우저 검증 재실행은 `src/modu_math_web/editor_next`에서 `npm run build` 후 `npm run test:teacher-browser`를 사용한다. 프로젝트 루트의 `.venv` Python과 설치된 Chrome을 사용하며, 다른 환경은 `MODU_TEST_PYTHON`, `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`를 지정하거나 Playwright Chromium을 설치한다. 사용자 DB/원본 문제와 실행 중인 서버에는 접근하지 않고 테스트 전용 서버를 종료한다.
