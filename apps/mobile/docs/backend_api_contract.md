# Modu Math Backend API Contract

This contract defines the first Django REST Framework boundary for the Flutter
client. The client must not send OpenAI API keys, model names, provider tokens,
or tutor system prompts. AI calls happen only behind the backend.

## Scope

Phase 2 starts with only these backend capabilities:

- Authentication/session bootstrap
- Learning attempt recording and basic progress reads
- AI tutor proxy

Payments, admin publishing, teacher assignment, and advanced operations are out
of scope for this contract.

## Common Rules

Base path: `/api/v1`

All JSON requests use:

```http
Content-Type: application/json
```

Authenticated requests use:

```http
Authorization: Bearer <session_or_access_token>
```

Error responses use:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Human-readable message safe for the app UI.",
    "fields": {
      "answer": ["This field is required."]
    }
  }
}
```

The backend should avoid logging full student free text, full tutor prompts,
tokens, OpenAI request bodies, and personally identifying child data.

## Authentication

### POST `/auth/anonymous-session`

Creates or restores a lightweight child-safe session for MVP usage.

Request:

```json
{
  "deviceId": "locally-generated-install-id",
  "grade": 3,
  "displayName": "민준"
}
```

Response `201`:

```json
{
  "student": {
    "id": "stu_01J...",
    "grade": 3,
    "displayName": "민준",
    "targetDailyCount": 10
  },
  "token": "opaque-session-token",
  "expiresAt": "2026-08-21T00:00:00Z"
}
```

Notes:

- `displayName` is optional and should not require a legal name.
- Future parent consent can attach to the same student id.

## Learning Progress

### POST `/learning/attempts`

Records one final answer attempt. Correctness may be calculated on the client for
offline MVP, but the server should re-check when it has verified answer data.

Request:

```json
{
  "problemId": "S3_초등_3_008540",
  "unit": "곱셈과 나눗셈",
  "answer": "24",
  "isCorrect": true,
  "hintLevelUsed": 1,
  "timeSpentSeconds": 82,
  "errorCategory": "none",
  "answeredAt": "2026-07-22T08:50:00Z"
}
```

Response `201`:

```json
{
  "attempt": {
    "id": "att_01J...",
    "problemId": "S3_초등_3_008540",
    "isCorrect": true,
    "errorCategory": "none",
    "answeredAt": "2026-07-22T08:50:00Z"
  },
  "reviewSchedule": null
}
```

Allowed `errorCategory` values:

- `understanding_target`
- `understanding_given`
- `planning_concept`
- `planning_operation`
- `execution_calculation`
- `execution_representation`
- `review_condition`
- `review_unit`
- `none`

### GET `/learning/daily-summary?date=YYYY-MM-DD`

Response `200`:

```json
{
  "date": "2026-07-22",
  "totalAttempted": 10,
  "totalCorrect": 8,
  "accuracy": 0.8,
  "streakDays": 3
}
```

### GET `/learning/masteries`

Response `200`:

```json
{
  "masteries": [
    {
      "unit": "곱셈과 나눗셈",
      "totalAttempted": 12,
      "totalCorrect": 9,
      "accuracy": 0.75,
      "lastAttemptAt": "2026-07-22T08:50:00Z"
    }
  ]
}
```

### GET `/learning/review-queue`

Returns problems due for spaced repetition.

Response `200`:

```json
{
  "items": [
    {
      "problemId": "S3_초등_3_008540",
      "unit": "곱셈과 나눗셈",
      "lastAttemptId": "att_01J...",
      "lastAnsweredAt": "2026-07-19T08:50:00Z",
      "errorCategory": "execution_calculation",
      "dueAt": "2026-07-22T00:00:00Z"
    }
  ]
}
```

## AI Tutor Proxy

### POST `/tutor/messages`

The Flutter client sends problem context and the recent conversation. The backend
builds the provider prompt, calls the AI provider, filters unsafe or over-revealing
text, and returns one tutor message. The backend must not let the model override
deterministic answer grading.

Request:

```json
{
  "action": "hint",
  "problem": {
    "id": "S3_초등_3_008540",
    "grade": 3,
    "subject": "math",
    "unit": "곱셈과 나눗셈",
    "type": "word_problem",
    "title": "S3_초등_3_008540",
    "prompt": "문제 본문",
    "choices": ["18", "24", "30"],
    "correctAnswer": "24",
    "answerMap": {},
    "semantic": {},
    "solvable": {}
  },
  "messages": [
    {
      "role": "student",
      "text": "나누면 되나요?",
      "replyType": null,
      "createdAt": "2026-07-22T08:51:00Z"
    }
  ],
  "hintLevel": 1
}
```

Allowed `action` values:

- `hint`
- `next_question`
- `respond`
- `review_answer`

Additional action fields:

- `hint`: `hintLevel`
- `next_question`: `stepIndex`
- `respond`: `message`, `stepIndex`
- `review_answer`: `answer`

Response `200`:

```json
{
  "message": {
    "role": "tutor",
    "text": "먼저 문제에서 구해야 하는 수가 무엇인지 다시 찾아볼까요?",
    "replyType": "hint",
    "createdAt": "2026-07-22T08:51:03Z"
  },
  "moderation": {
    "filtered": false
  }
}
```

Allowed `replyType` values:

- `greeting`
- `hint`
- `question`
- `correct`
- `retry`

Backend tutor requirements:

- Never expose the final answer only because the student asks.
- Use deterministic answer data for correctness.
- Record or return misconception categories separately from final grading.
- Prefer the sequence: condition check, concept link, operation choice, partial
  scaffolding, final explanation.
- Store only the minimal tutor telemetry required for learning analytics.

## Flutter Configuration

The client supports:

```dotenv
AI_TUTOR_MODE=mock
BACKEND_API_BASE_URL=http://localhost:8000
BACKEND_SESSION_TOKEN=
```

Use `AI_TUTOR_MODE=backend` only when the DRF server is available. OpenAI keys
belong only in backend environment variables.
