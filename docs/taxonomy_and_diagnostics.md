# Modu Math 개념·기능 체계 및 진단 분석 시스템 문서

본 문서는 Modu Math 프로젝트의 **초등 수학 개념·기능 체계(Taxonomy)**, **규칙 기반 문제 자동 태깅(Auto-tagging)**, **설명 가능한 숙련도 및 진단 분석 엔진(Mastery & Diagnostics Engine)**, **추천 엔진**, **Flutter 모바일 연동**, **테스트 데이터 시딩 및 관리자 운영 가이드**를 설명합니다.

---

## 1. 개념 및 기능 체계표 (Taxonomy)

체계 정의는 [`src/modu_math/taxonomy/taxonomy.json`](file:///c:/projects/modu_math/src/modu_math/taxonomy/taxonomy.json)에 정의되어 있으며, Python의 [`TaxonomyRegistry`](file:///c:/projects/modu_math/src/modu_math/taxonomy/__init__.py) 싱글톤을 통해 로드·검증됩니다.

### 1.1 개념 체계 (Concepts)
개념은 초등 수학 교육과정의 영역(수와 연산, 도형, 측정, 규칙성, 자료와 가능성)을 계층형 도트 표기법(`domain.subdomain.concept`)으로 분류합니다.

| 분류 ID | 명칭 | 학년군 | 상위 개념 | 설명 |
|---|---|---|---|---|
| `arithmetic.addition.single_digit` | 한 자리 수 덧셈 | 초등 1~2학년 | `arithmetic.addition` | 10 이하 및 한 자리 수의 합 |
| `arithmetic.addition.multi_digit` | 여러 자리 수 덧셈 | 초등 1~3학년 | `arithmetic.addition` | 받아올림이 있는 두 자리 이상 수의 덧셈 |
| `arithmetic.addition.with_regrouping` | 받아올림이 있는 덧셈 | 초등 2~3학년 | `arithmetic.addition.multi_digit` | 자릿수 올림(Carry) 연산 |
| `arithmetic.subtraction.single_digit` | 한 자리 수 뺄셈 | 초등 1~2학년 | `arithmetic.subtraction` | 한 자리 수 사이의 차 |
| `arithmetic.subtraction.with_regrouping`| 받아내림이 있는 뺄셈 | 초등 2~3학년 | `arithmetic.subtraction` | 자릿수 빌림(Borrow) 연산 |
| `arithmetic.multiplication.tables` | 구구단 (곱셈구구) | 초등 2~3학년 | `arithmetic.multiplication` | 2단~9단 곱셈구구 기본 암기 및 계산 |
| `arithmetic.multiplication.multi_digit`| 여러 자리 수 곱셈 | 초등 3~4학년 | `arithmetic.multiplication` | 두 자리 × 한 자리, 두 자리 × 두 자리 곱셈 |
| `arithmetic.division.basic` | 기초 나눗셈 | 초등 3~4학년 | `arithmetic.division` | 구구단 범위 내 몫과 나머지 구하기 |
| `arithmetic.division.long_division` | 세로셈 나눗셈 | 초등 3~4학년 | `arithmetic.division` | 두 자리 ÷ 한 자리, 세 자리 ÷ 두 자리 나눗셈 |
| `arithmetic.fractions.concept` | 분수의 기초 개념 | 초등 3~4학년 | `arithmetic.fractions` | 전체에 대한 부분, 단위분수, 진분수 |
| `arithmetic.fractions.addition_subtraction`| 동모분수 덧셈과 뺄셈 | 초등 3~5학년 | `arithmetic.fractions` | 분모가 같은 분수의 계산 |
| `arithmetic.decimals.concept` | 소수의 기초 개념 | 초등 3~4학년 | `arithmetic.decimals` | 0.1, 소수 첫째 자리, 자릿값 이해 |
| `geometry.shapes.2d_basic` | 기본 평면도형 | 초등 1~2학년 | `geometry.shapes` | 삼각형, 사각형, 원의 모양과 특징 |
| `geometry.shapes.quadrilaterals` | 다각형과 사각형 | 초등 3~4학년 | `geometry.shapes` | 직사각형, 정사각형, 사다리꼴, 평행사변형 |
| `geometry.angles` | 각과 각도 | 초등 3~4학년 | `geometry` | 예각, 직각, 둔각, 각도 측정 |
| `geometry.perimeter_and_area` | 둘레와 넓이 | 초등 4~5학년 | `geometry` | 직사각형 둘레, $1\text{cm}^2$, 넓이 공식 |
| `measurement.time.reading_clock` | 시계 보기와 시각 | 초등 1~2학년 | `measurement.time` | 몇 시, 몇 분, 5분 단위 읽기 |
| `measurement.time.time_intervals` | 시간의 계산 | 초등 2~3학년 | `measurement.time` | 시작 시각, 걸린 시간, 끝난 시각 계산 |
| `measurement.length` | 길이와 거리 측정 | 초등 2~3학년 | `measurement` | mm, cm, m, km 단위 변환과 어림 |
| `measurement.weight_and_capacity` | 무게와 들이 | 초등 3학년 | `measurement` | g, kg, mL, L 단위 이해와 합/차 |
| `patterns.number_sequences` | 수 배열의 규칙 | 초등 1~3학년 | `patterns` | 등차 규칙, 뛰어 세기, 빈칸 채우기 |
| `data.tables_and_graphs` | 표와 그래프 | 초등 2~4학년 | `data` | 표 해석, 막대그래프, 그림그래프 읽기 |

### 1.2 기능 체계 (Skills)
기능은 문제를 해결할 때 발휘되는 인지적 행동 및 절차적 능력을 정의합니다.

| 기능 ID | 명칭 | 범주 | 설명 |
|---|---|---|---|
| `skill.calculation.mental` | 암산 능력 | `calculation` | 머릿속으로 단순 연산을 신속히 처리하는 능력 |
| `skill.calculation.procedural` | 절차적 필산 능력 | `calculation` | 세로셈, 받아올림/받아내림 등 정해진 계산 절차 수행 |
| `skill.representation.word_to_equation` | 문장제 식 세우기 | `representation`| 실생활 문장제 상황을 덧셈/뺄셈/곱셈/나눗셈 식으로 변환 |
| `skill.representation.visual_model` | 시각적 모델 활용 | `representation`| 수직선, 블록, 모눈, 묶음 그림을 활용한 모델링 |
| `skill.problem_solving.step_by_step` | 단계적 추론 | `problem_solving`| 복합 단계 문제에서 순서대로 중간값을 도출하는 능력 |
| `skill.problem_solving.pattern_discovery`| 규칙 발견과 일반화 | `problem_solving`| 수나 도형의 배열에서 일정한 패턴을 찾는 능력 |
| `skill.verification.estimation` | 어림하기 및 결과 검증 | `verification` | 답의 크기나 단위를 미리 어림하고 타당성을 검토 |
| `skill.geometry.shape_identification` | 도형 식별 및 구성요소 파악 | `geometry` | 변, 꼭짓점, 각, 대각선 등 기하학적 요소 구별 |
| `skill.measurement.unit_conversion` | 단위 환산 | `measurement` | cm $\leftrightarrow$ m, 분 $\leftrightarrow$ 초 등 단위 환산 |
| `skill.data.graph_reading` | 그래프 및 도표 읽기 | `data_literacy` | 차트 축, 눈금, 범례를 읽고 필요한 정보를 추출 |

---

## 2. 규칙 기반 자동 태깅 (Rule-based Auto-Tagger)

[`ProblemAutoTagger`](file:///c:/projects/modu_math/src/modu_math/taxonomy/tagger.py)는 불투명한 딥러닝 모델 대신 **명확한 규칙, 키워드 매핑, DSL 메타데이터, solvable 연산자 분석**을 통해 문제를 태깅합니다.

### 2.1 판정 로직
1. **Source 1: 기존 Semantic Metadata 매핑**
   - 문제 JSON의 `metadata.concepts`, `metadata.skills`, `metadata.domain`, `metadata.topic` 파싱
   - 기존 한글/영문 태그(예: `한자리수덧셈`, `addition`, `word_problem`)를 정규화하여 Taxonomy ID로 매핑.
2. **Source 2: Solvable 수식 및 연산 분석**
   - solvable 스텝의 `operation` (`add`, `sub`, `mul`, `div`), `method`, `step_type` 분석.
   - 받아올림(`carry`/`regrouping`), 분수 수식(`fractions`), 시계/시간 모델 검출.
3. **Source 3: 문제 텍스트(한국어 형태) 정규식/키워드 분석**
   - 텍스트 키워드 규칙 매칭:
     - 덧셈: "더하", "합하", "모두", "합계", "몇 개가 됩니까"
     - 뺄셈: "남은", "빼", "차", "몇 개 더 많", "덜어내"
     - 곱셈: "묶음", "배", "구구", "곱하"
     - 나눗셈: "똑같이 나누", "몫", "나머지"
     - 도형: "삼각형", "사각형", "원", "직각", "변", "꼭짓점"
     - 측정: "시계", "몇 시", "몇 분", "길이", "cm", "m", "kg", "무게"
4. **Source 4: 기능(Skills) 유추 규칙**
   - 문장제(스토리텔링, 2문장 이상 또는 실생활 맥락) $\rightarrow$ `skill.representation.word_to_equation`
   - solvable에 단계가 2단계 이상 $\rightarrow$ `skill.problem_solving.step_by_step`
   - 다자리 수 계산 $\rightarrow$ `skill.calculation.procedural`
   - 이미지/다이어그램 레이아웃 포함 $\rightarrow$ `skill.representation.visual_model`
5. **신뢰도(Confidence) 산출**
   - 점수 가산제:
     - 메타데이터 태그 일치: +0.40
     - 텍스트 키워드 매칭: +0.35
     - Solvable 연산 구조 일치: +0.25
   - Confidence $\ge 0.70$: 자동 확인(또는 고신뢰도) 상태
   - Confidence $< 0.70$: 검토 필요(`needs_review`) 플래그 부여

### 2.2 룰 버전 관리
- `ProblemTagging` 모델에 `rule_version` 필드를 두어 태깅에 적용된 규칙 버전(기본 `v1.0.0`)을 추적합니다.
- 규칙 사전이 업데이트될 경우 `--overwrite-confirmed` 플래그 없이 실행하면 관리자가 검토 확정(`confirmed`)한 태그는 보존되고, 미확정(`unreviewed`, `needs_review`) 태그만 신규 버전으로 재태깅됩니다.

---

## 3. 설명 가능한 숙련도 및 진단 분석 공식

### 3.1 숙련도 공식 (Bayesian Smoothed Score with Penalties)

학생의 숙련도 $M$은 0.0에서 1.0 사이의 실수값으로 산출되며, 적은 풀이 횟수로 인한 극단값 왜곡을 방지하기 위해 베이지안 스무딩(Bayesian Smoothing)을 적용합니다.

$$M_0 = 0.5 \quad (\text{사전 숙련도 평균})$$
$$W = 2.0 \quad (\text{사전 관측 가중치, 의사 시도 횟수})$$

각 시도 $i$에 대한 유효 정답값 $S_i$는 다음과 같이 계산됩니다:

$$S_i = \begin{cases} 
\max\left(0.2,\, 1.0 - (0.15 \times \text{hint\_count}) - (0.10 \times \text{retry\_count})\right) & \text{if 정답} \\ 
0.0 & \text{if 오답}
\end{cases}$$

누적 유효 정답 점수의 합 $\tilde{C} = \sum_{i=1}^{N} S_i$ 에 대해, 베이지안 평활화 숙련도 $M$은 다음과 같습니다:

$$M = \frac{(M_0 \times W) + \tilde{C}}{W + N} = \frac{1.0 + \tilde{C}}{2.0 + N}$$

### 3.2 신뢰도 지수 (Confidence Score)
풀이 표본 수 $N$에 따른 데이터 신뢰도 $C_{\text{rate}}$:

$$C_{\text{rate}} = \min\left(1.0,\, \frac{N}{5.0}\right)$$

- $N \ge 5$ 이면 신뢰도 100% (충분한 진단 표본 확보)
- $N < 3$ 이면 진단 UI에서 "표본 수집 중" 뱃지 표시

### 3.3 강점과 취약점 판정 기준
- **강점(Strengths)**:
  - 시도 횟수 $N \ge 2$ 이고 숙련도 $M \ge 0.75$
  - 숙련도 내림차순 상위 최대 5개 선정
- **취약점(Weaknesses)**:
  - 시도 횟수 $N \ge 1$ 이고 숙련도 $M < 0.60$
  - 숙련도 오름차순(가장 취약한 항목) 상위 최대 5개 선정

---

## 4. 추천 엔진 알고리즘 (Recommendation Engine)

`ProblemRecommendationService`는 학생의 숙련도 프로필에 따라 5단계 우선순위로 개인화된 문제를 선별합니다:

1. **우선순위 1 (취약점 집중 보완)**:
   - 학생의 가장 취약한 개념($M < 0.60$)에 속하면서 아직 맞히지 못한 문제
2. **우선순위 2 (최근 오답 문제 복습)**:
   - 최근 풀이에서 오답을 기록한 동일 또는 유사 문제
3. **우선순위 3 (적정 난이도 도전)**:
   - 중간 숙련도($0.60 \le M \le 0.80$) 영역에서 학습 진도를 확장할 수 있는 미해결 문제
4. **우선순위 4 (새로운 개념 탐색)**:
   - 학생이 한 번도 시도하지 않은 기초 개념 문제
5. **우선순위 5 (강점 유지 및 복습)**:
   - 강점 개념의 심화 문제

---

## 5. API 명세 및 JSON 예시

### 5.1 `GET /api/v1/diagnostics/summary/`
- **인증**: `Authorization: Token <token>`
- **설명**: 학생의 전체 풀이 통계, 종합 숙련도, 강점/취약점 목록 반환.
- **응답 예시**:
```json
{
  "total_attempts": 24,
  "correct_attempts": 19,
  "accuracy_rate": 0.792,
  "average_mastery": 0.764,
  "overall_status": "good",
  "evaluated_concepts_count": 8,
  "evaluated_skills_count": 5,
  "strengths": [
    {
      "tag": "arithmetic.addition.single_digit",
      "name": "한 자리 수 덧셈",
      "type": "concept",
      "mastery_score": 0.91,
      "attempts_count": 8,
      "correct_count": 8
    }
  ],
  "weaknesses": [
    {
      "tag": "arithmetic.subtraction.with_regrouping",
      "name": "받아내림이 있는 뺄셈",
      "type": "concept",
      "mastery_score": 0.42,
      "attempts_count": 4,
      "correct_count": 1
    }
  ],
  "recent_activity": {
    "total_elapsed_seconds": 380,
    "last_solved_at": "2026-09-12T09:15:30Z"
  }
}
```

### 5.2 `GET /api/v1/diagnostics/concepts/`
- **인증**: `Authorization: Token <token>`
- **설명**: 개념별 상세 숙련도, 시도 횟수, 신뢰도 지수 반환.

### 5.3 `GET /api/v1/diagnostics/skills/`
- **인증**: `Authorization: Token <token>`
- **설명**: 기능별 상세 숙련도 목록 반환.

### 5.4 `GET /api/v1/diagnostics/history/`
- **인증**: `Authorization: Token <token>`
- **쿼리 파라미터**: `days` (기본값: 14)
- **설명**: 일자별 풀이 횟수, 정답 횟수, 일일 정답률 추이 반환.

### 5.5 `GET /api/v1/recommendations/`
- **인증**: `Authorization: Token <token>`
- **쿼리 파라미터**: `limit` (기본값: 5)
- **응답 예시**:
```json
{
  "count": 3,
  "recommendations": [
    {
      "problem": {
        "id": 14,
        "problem_id": "math-sub-regroup-01",
        "title": "받아내림 뺄셈 연습",
        "grade": 3,
        "difficulty": "medium",
        "concepts": ["arithmetic.subtraction.with_regrouping"],
        "skills": ["skill.calculation.procedural"]
      },
      "reason": "취약 개념 '받아내림이 있는 뺄셈' 보완이 필요합니다.",
      "priority_tier": 1,
      "target_concept": "arithmetic.subtraction.with_regrouping"
    }
  ]
}
```

### 5.6 관리자 태그 검토 API (`IsAdminUser`)
- `GET /api/v1/admin/problem-tags/` : 문제별 태그 상태 목록 (필터: `review_status`, `low_confidence`)
- `PATCH /api/v1/admin/problem-tags/{id}/` : 태그 수정 (`reviewed_concepts`, `reviewed_skills`)
- `POST /api/v1/admin/problem-tags/{id}/confirm/` : 검토 확정 처리 (`review_status = "confirmed"`)

---

## 6. Flutter 모바일 연동 가이드

### 6.1 서비스 구조
- `AuthService` (`apps/mobile/lib/services/auth_service.dart`):
  - 백엔드 `TokenAuthentication`과 통신.
  - 로그인 성공 시 DRF 토큰 및 사용자 프로필을 `SharedPreferences`에 안전하게 영구 저장.
- `BackendAttemptService` (`apps/mobile/lib/services/backend_attempt_service.dart`):
  - **오프라인 큐**: 네트워크 단절 시 시도 기록을 로컬 큐에 저장 후, 네트워크 복구 시 자동 동기화.
  - **서버 권위 채점**: 클라이언트가 보낸 임의의 판정값은 무시되며, 서버 응답의 `is_correct`로 채점 결과를 확정.
- `DiagnosticsService` (`apps/mobile/lib/services/diagnostics_service.dart`):
  - 5개 진단 엔드포인트와 통신하여 실시간 숙련도와 추천 문제 목록을 불러옴.

### 6.2 화면 구성
- `AuthScreen` (`apps/mobile/lib/screens/auth_screen.dart`):
  - 학생 로그인 및 회원가입 탭 UI 제공.
- `DiagnosticScreen` (`apps/mobile/lib/screens/diagnostic_screen.dart`):
  - **종합 요약 카드**: 전체 정확도, 총 풀이 수, 평가 개념 수
  - **맞춤 추천 문제 섹션**: "바로 풀기" 버튼 클릭 시 `ProblemSolveScreen`으로 즉시 라우팅
  - **강점 및 보완점 카드**: 색상 태그 및 점수 시각화
  - **개념·기능별 숙련도 게이지**: 진행 바 및 백분율 표시
  - **최근 7일 학습 활동 추이 차트**: 막대 그래프로 일자별 성취도 확인

---

## 7. 테스트 계정 생성 및 샘플 데이터 시딩

### 7.1 문제 태깅 일괄 실행
```bash
# 전체 문제에 대해 자동 태깅 실행
uv run python manage.py tag_problems

# 신뢰도가 0.7 미만인 문제만 확인
uv run python manage.py tag_problems --low-confidence

# 특정 문제만 재태깅
uv run python manage.py tag_problems --problem-id 1
```

### 7.2 테스트 계정 및 풀이 데이터 생성 스크립트
Django shell을 사용하여 테스트용 학생 계정과 시도 데이터를 생성할 수 있습니다:

```bash
uv run python manage.py shell
```

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from modu_math_web.learning.models import Problem, Attempt

# 1. 테스트 사용자 생성
user, created = User.objects.get_or_create(username="test_student", email="student@example.com")
if created:
    user.set_password("student123!")
    user.save()
token, _ = Token.objects.get_or_create(user=user)
print(f"User: {user.username}, Token: {token.key}")

# 2. 샘플 풀이 데이터 등록 (맞춤 추천 및 진단 활성화용)
problems = Problem.objects.all()[:5]
for idx, p in enumerate(problems):
    is_correct = (idx % 2 == 0)
    Attempt.objects.create(
        user=user,
        problem=p,
        submitted_answer={"value": "answer"},
        is_correct=is_correct,
        elapsed_ms=5000 + idx * 1000,
        hint_count=0 if is_correct else 1,
        retry_count=0,
    )
print(f"{problems.count()} attempts seeded.")
```

---

## 8. 관리자 검토 및 확정 (Admin Review)

### 8.1 CLI 관리 명령 활용
```bash
# 확정된 태그를 제외하고 재태깅
uv run python manage.py tag_problems

# 관리자 검토 완료 태그까지 강제 덮어쓰기
uv run python manage.py tag_problems --overwrite-confirmed
```

### 8.2 관리자 API 활용
슈퍼유저 또는 스태프 계정의 토큰으로 다음 엔드포인트를 호출합니다:

```bash
# 1. 검토가 필요한 태그 목록 조회
curl -H "Authorization: Token <admin_token>" \
  "http://localhost:8000/api/v1/admin/problem-tags/?review_status=needs_review"

# 2. 태그 수정 및 저장
curl -X PATCH "http://localhost:8000/api/v1/admin/problem-tags/14/" \
  -H "Authorization: Token <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewed_concepts": ["arithmetic.subtraction.with_regrouping"],
    "reviewed_skills": ["skill.calculation.procedural"]
  }'

# 3. 태그 최종 확정 (Confirmed)
curl -X POST "http://localhost:8000/api/v1/admin/problem-tags/14/confirm/" \
  -H "Authorization: Token <admin_token>"
```
