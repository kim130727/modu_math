# 한국어 원본 기반 우크라이나어 현지화

현재 지원 언어는 한국어(`ko`)와 우크라이나어(`uk`)입니다. 문제 저작 데이터는
문제당 하나의 통합 문서를 사용하며, `locales/` 같은 별도 번역 트리는 사용하지
않습니다.

## 저장 구조

```text
examples/problems/
└── ko/
    ├── <problem>.dsl.py       # 한국어 구조·콘텐츠 원본
    └── <problem>.i18n.json    # 공통 편집 정보와 uk 번역·차이 데이터

apps/mobile/assets/i18n/
├── ko.json                    # 앱 UI 한국어
└── uk.json                    # 앱 UI 우크라이나어

apps/mobile/generated/examples/problems/
├── ko/                        # 폐기 후 재생성 가능한 한국어 빌드 결과
└── uk/                        # 폐기 후 재생성 가능한 우크라이나어 빌드 결과
```

`examples/problems/uk/<problem>.dsl.py`는 실제 파일이 아니라 통합 문서에서 합성되는
가상 경로입니다. 따라서 한국어와 우크라이나어 Python 원본이 서로 달라지는 문제를
방지합니다.

통합 문서의 핵심 구조는 다음과 같습니다.

```json
{
  "version": 2,
  "source_language": "ko",
  "editor_overrides": {},
  "languages": {
    "uk": {
      "translation_catalog": {},
      "delta": {},
      "editor_overrides": {}
    }
  }
}
```

- `translation_catalog`: 한국어 원문과 우크라이나어 번역의 대응표
- `delta`: 한국어 DSL과 다른 우크라이나어 필드만 저장한 실제 언어 변형
- `editor_overrides`: 언어별 배치 보정
- `generated/`: 앱이 읽는 빌드 결과이며 저작 원본이 아님

## 권장 작업 흐름

1. 한국어 탭에서 DSL 원본을 편집하고 저장합니다.
2. 번역 카탈로그를 갱신합니다.

   ```powershell
   .venv\Scripts\python.exe tools/extract_dsl_localization.py `
     --dsl examples/problems/ko/<problem>.dsl.py `
     --locale uk
   ```

   통합된 문제에서는 별도 파일을 만들지 않고 같은 이름의 `*.i18n.json` 안에
   `languages.uk.translation_catalog`를 생성하거나 갱신합니다.

3. 웹에디터의 우크라이나어 탭에서 번역을 편집하는 것을 권장합니다. 카탈로그를
   외부에서 수정했다면 다음 명령으로 번역을 언어 변형에 반영할 수 있습니다.

   ```powershell
   .venv\Scripts\python.exe tools/apply_dsl_localization.py `
     --dsl examples/problems/ko/<problem>.dsl.py `
     --i18n-json examples/problems/ko/<problem>.i18n.json `
     --locale uk `
     --force
   ```

4. 웹에디터에서 Build를 실행합니다. 한국어 원본을 Build하면 연결된 우크라이나어
   문제도 갱신됩니다. 모바일 오프라인 번들은 다음 명령으로 내보냅니다.

   ```powershell
   .venv\Scripts\python.exe tools/export_problem_content.py
   ```

5. 앱의 언어 전환은 UI 문자열을 `assets/i18n/uk.json`에서, 문제 콘텐츠를
   `generated/examples/problems/uk/`에서 읽습니다. 앱이 `*.i18n.json`이나 번역
   카탈로그를 실행 중에 직접 번역하지는 않습니다.

## 일관성 원칙

- 사람이 관리하는 문제 원본은 한국어 DSL과 문제별 통합 JSON뿐입니다.
- 우크라이나어는 한국어 공통 구조를 상속하고 다른 값만 저장합니다.
- 원문이 바뀌어 번역 대상이 달라지면 기존 번역을 자동 적용하지 않고 검토 대상으로
  남깁니다.
- 독립적인 실험용 DSL에서만 `extract_dsl_localization.py --out ...`으로 standalone
  카탈로그를 만들 수 있습니다. 프로젝트 문제에는 사용하지 않습니다.
- `apps/mobile/generated/`와 캐시는 언제든 다시 만들 수 있는 산출물입니다.

## 레거시 데이터 이전

이전 버전의 `*.locale-delta.json`, 언어별 DSL, `locales/*/*.locale.json`을 가져올 때만
다음 마이그레이션 도구를 사용합니다.

```powershell
.venv\Scripts\python.exe tools/consolidate_problem_json.py `
  examples/problems --catalogs locales
```

결과와 렌더링 검증이 끝난 뒤에만 `--delete`를 추가합니다. 이미 통합된 문제에는 이
명령을 다시 실행하지 않습니다.
