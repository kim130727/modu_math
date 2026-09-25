# 한국어 원본 기반 우크라이나어 현지화

지원 언어는 한국어(`ko`)와 우크라이나어(`uk`)입니다. 한국어 DSL을 유일한 문제
구조 원본으로 사용하고, 번역과 화면 배치는 서로 다른 파일에 저장합니다.

## 저장 구조

```text
examples/problems/ko/
└── <problem>.dsl.py                 # 한국어 문제 원본

locales/uk/
└── <problem>.json                   # 한국어 → 우크라이나어 문장

overrides/
├── ko/<problem>.layout.json         # 한국어 배치 보정
└── uk/<problem>.layout.json         # 우크라이나어 배치 보정

apps/mobile/generated/examples/problems/
├── ko/                              # 재생성 가능한 앱 콘텐츠
└── uk/
```

정답 검토 상태가 필요한 문제만 `overrides/uk/<problem>.review.json`을 사용합니다.
빌드 캐시와 이전 생성 이력은 `.modu-cache/`에 저장되며 저작 원본이 아닙니다.

## 번역 파일

번역자가 다루는 파일은 `locales/uk`뿐입니다.

```json
{
  "version": 1,
  "problem_id": "S3_elem_3_008540",
  "source_language": "ko",
  "target_language": "uk",
  "strings": {
    "template.title": {
      "source": "알맞은 식을 고르세요.",
      "translation": "Виберіть правильний вираз."
    }
  }
}
```

`source`가 바뀌면 에디터가 번역 검토 대상으로 표시합니다. 번역 파일에는 좌표,
폰트 크기, 생성된 SVG, 전체 문제 복사본을 넣지 않습니다.

## 작업 흐름

1. `examples/problems/ko/<problem>.dsl.py`에서 한국어 문제를 편집합니다.
2. 번역 대상 문장을 갱신합니다.

   ```powershell
   .venv\Scripts\python.exe tools/extract_dsl_localization.py `
     --dsl examples/problems/ko/<problem>.dsl.py `
     --locale uk
   ```

3. `locales/uk/<problem>.json`의 `translation` 값만 번역합니다.
4. 웹에디터 우크라이나어 화면에서 위치를 조정하면
   `overrides/uk/<problem>.layout.json`에 저장됩니다.
5. 모바일 콘텐츠를 내보냅니다.

   ```powershell
   .venv\Scripts\python.exe tools/export_problem_content.py
   ```

앱은 실행 중에 번역하지 않습니다. 한국어 DSL, locale, layout override를 합쳐서
생성한 `generated/examples/problems/{ko,uk}` 콘텐츠를 언어 선택에 맞춰 읽습니다.

## 저장 원칙

- 문제 구조와 계산 논리는 한국어 DSL에 한 번만 저장합니다.
- 우크라이나어 locale에는 원문과 번역문만 저장합니다.
- 언어별 좌표와 글자 크기는 layout override에 저장합니다.
- locale에서 만든 번역을 별도의 `delta`에 중복 저장하지 않습니다.
- 생성 파일과 캐시는 삭제 후 다시 만들 수 있어야 합니다.
- `*.i18n.json`은 사용하지 않습니다.

## 이전 형식 마이그레이션

과거 `*.i18n.json` 자료를 가져올 때만 다음 도구를 사용합니다.

```powershell
.venv\Scripts\python.exe tools/split_i18n_storage.py examples/problems
```

결과를 검증한 뒤 기존 문서까지 제거하려면 `--delete`를 추가합니다.
