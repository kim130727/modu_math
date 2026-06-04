# 0) 변수 설정 (PowerShell 예약변수 PID 충돌 방지)
$PROB_ID = "<YOUR_PROB_ID>"
$DIR = "examples/problems/<PROBLEM_DIR>"
$IMG = "$DIR/$PROB_ID.png"

# 1) vision draft 프롬프트 생성 (llm-output 없으면 정상 종료)
python tools/generate_vision_draft.py `
  --image "$IMG" `
  --problem-id "$PROB_ID" `
  --out "$DIR/$PROB_ID.vision_draft.md" `
  --mode prompt `
  --provider openai `
  --prompt-out "$DIR/$PROB_ID.vision_prompt.md" `
  --force

# 2) 응답 텍스트로 vision draft 생성
# $DIR/$PROB_ID.vision_llm_output.txt
python tools/generate_vision_draft.py `
  --image "$IMG" `
  --problem-id "$PROB_ID" `
  --out "$DIR/$PROB_ID.vision_draft.md" `
  --mode prompt `
  --provider openai `
  --llm-output-file "$DIR/$PROB_ID.vision_llm_output.txt" `
  --force

# 3) refined draft 프롬프트 생성 (llm-output 없으면 정상 종료)
python tools/refine_vision_draft.py `
  --vision-draft "$DIR/$PROB_ID.vision_draft.md" `
  --problem-id "$PROB_ID" `
  --image "$IMG" `
  --out "$DIR/$PROB_ID.refined_draft.md" `
  --mode prompt `
  --provider openai `
  --prompt-out "$DIR/$PROB_ID.refine_prompt.md" `
  --force

# 4) 응답 텍스트로 refined draft 생성
# $DIR/$PROB_ID.refine_llm_output.txt
python tools/refine_vision_draft.py `
  --vision-draft "$DIR/$PROB_ID.vision_draft.md" `
  --problem-id "$PROB_ID" `
  --image "$IMG" `
  --out "$DIR/$PROB_ID.refined_draft.md" `
  --mode prompt `
  --provider openai `
  --llm-output-file "$DIR/$PROB_ID.refine_llm_output.txt" `
  --force

# 5) DSL 프롬프트 생성 (llm-output 없으면 정상 종료)
python tools/generate_dsl_from_refined_draft.py `
  --draft "$DIR/$PROB_ID.refined_draft.md" `
  --image "$IMG" `
  --problem-id "$PROB_ID" `
  --out "$DIR/$PROB_ID.dsl.py" `
  --mode prompt `
  --provider openai `
  --system-prompt "prompts/dsl_agent_system.md" `
  --rules-md "prompts/dsl_generation_rules.md" `
  --prompt-out "$DIR/$PROB_ID.dsl_prompt.md" `
  --force

# 6) 응답 텍스트로 DSL 파일 생성
# 주석은 빼고 코드만 그대로 복사해서, 가독성 있게 전체를 텍스트 파일로 정리
# $DIR/$PROB_ID.dsl_llm_output.txt
python tools/generate_dsl_from_refined_draft.py `
  --draft "$DIR/$PROB_ID.refined_draft.md" `
  --image "$IMG" `
  --problem-id "$PROB_ID" `
  --out "$DIR/$PROB_ID.dsl.py" `
  --mode prompt `
  --provider openai `
  --llm-output-file "$DIR/$PROB_ID.dsl_llm_output.txt" `
  --system-prompt "prompts/dsl_agent_system.md" `
  --rules-md "prompts/dsl_generation_rules.md" `
  --force

# 7) JSON/SVG 추출 + 검증
python tools/validate_generated_dsl.py `
  --dsl "$DIR/$PROB_ID.dsl.py" `
  --out-prefix "$DIR/$PROB_ID" `
  --strict `
  --emit-solvable `
  --report "$DIR/$PROB_ID.build_report.json"

# 8) 최종 mb 확인
mb $PROB_ID

## JSON Naming Guard

- `source problem json`: original dataset-side JSON (same basename as PNG).
- `semantic/layout/renderer/solvable json`: pipeline-generated artifacts.

Rule:

- If original JSON exists, use it only as reference context.
- Do not overwrite or reinterpret original JSON as generated semantic/layout/renderer JSON.
