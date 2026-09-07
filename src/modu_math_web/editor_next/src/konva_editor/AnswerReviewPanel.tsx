import { useEffect, useState } from "react";
import { normalizedAnswer, type AnswerReviewSettings } from "./answerReview";

export function AnswerReviewPanel({
  settings,
  onChange,
  onSave,
  onSelect,
  onEditLayout,
  busy,
  feedback,
}: {
  settings: AnswerReviewSettings;
  onChange: (settings: AnswerReviewSettings) => void;
  onSave: (override?: AnswerReviewSettings) => void;
  onSelect: (ids: string[]) => void;
  onEditLayout: () => void;
  busy: boolean;
  feedback?: string;
}) {
  const [editing, setEditing] = useState(false);
  const [responses, setResponses] = useState<string[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [result, setResult] = useState<string | null>(null);
  const [customInputAnswer, setCustomInputAnswer] = useState("");
  const [showInputEdit, setShowInputEdit] = useState(false);

  useEffect(() => {
    setResponses([]);
    setSelected([]);
    setResult(null);
    setCustomInputAnswer("");
    setShowInputEdit(false);
  }, [settings]);

  const update = (patch: Partial<AnswerReviewSettings>) => onChange({ ...settings, ...patch });

  const choiceMode = settings.mode === "choice";
  const groupMode = settings.mode === "grouped_choice";
  const oxMode = settings.mode === "ox";
  const groups = settings.groups ?? [];
  const expected = settings.choices.filter((choice) => choice.correct).map((choice) => choice.id);

  const hasAnswers = groupMode
    ? groups.length > 0 &&
      groups.every(
        (group) => group.choices.length >= 2 && group.correct_index >= 0 && group.correct_index < group.choices.length,
      )
    : choiceMode
      ? expected.length > 0 && settings.choices.length >= 2 && settings.choices.every((choice) => choice.text.trim())
      : settings.answers.length > 0 &&
        settings.answers.every((answer) => (oxMode ? /^[OX]$/.test(answer.value) : answer.value.trim().length > 0));

  const check = () => {
    const correct = groupMode
      ? groups.every((group, index) => responses[index] === String(group.correct_index))
      : choiceMode
        ? expected.length === selected.length && expected.every((id) => selected.includes(id))
        : settings.answers.every((answer, index) => normalizedAnswer(responses[index] ?? "") === normalizedAnswer(answer.value));
    setResult(correct ? "✓ 정답입니다! (채점 일치)" : "✕ 정답과 다릅니다. 입력 내용과 등록된 정답을 확인하세요.");
  };

  const setChoiceAsCorrectAndSave = (choiceId: string) => {
    const next: AnswerReviewSettings = {
      ...settings,
      status: "verified",
      choices: settings.choices.map((c) => ({ ...c, correct: c.id === choiceId })),
    };
    onChange(next);
    onSave(next);
  };

  const setSelectedChoicesAsCorrectAndSave = () => {
    if (!selected.length) return;
    const next: AnswerReviewSettings = {
      ...settings,
      status: "verified",
      choices: settings.choices.map((c) => ({ ...c, correct: selected.includes(c.id) })),
    };
    onChange(next);
    onSave(next);
  };

  const registerDirectInputAnswerAndSave = (valueText: string) => {
    const trimmed = valueText.trim();
    if (!trimmed) return;
    const next: AnswerReviewSettings = {
      ...settings,
      status: "verified",
      answers: [{ value: trimmed, ref: "answer.value" }],
    };
    onChange(next);
    onSave(next);
  };

  const registerOxAnswersAndSave = () => {
    const valid = responses.length > 0 && responses.every((r) => /^[OX]$/.test(r));
    if (!valid) return;
    const next: AnswerReviewSettings = {
      ...settings,
      status: "verified",
      answers: responses.map((r) => ({ value: r })),
    };
    onChange(next);
    onSave(next);
  };

  const registerGroupChoicesAndSave = () => {
    const valid = groups.length > 0 && groups.every((_, i) => responses[i] !== undefined && responses[i] !== "");
    if (!valid) return;
    const next: AnswerReviewSettings = {
      ...settings,
      status: "verified",
      groups: groups.map((g, i) => ({ ...g, correct_index: Number(responses[i]) })),
    };
    onChange(next);
    onSave(next);
  };

  const registeredAnswerSummary = () => {
    if (groupMode) {
      return groups.map((g) => `${g.label}: ${g.choices[g.correct_index] ?? "미등록"}`).join(" | ");
    }
    if (choiceMode) {
      const correctChoices = settings.choices.filter((c) => c.correct);
      return correctChoices.length
        ? correctChoices.map((c) => `${c.label} ${c.text}`).join(", ")
        : "미등록";
    }
    if (oxMode || settings.mode === "panel_input" || settings.mode === "canvas_slots") {
      return settings.answers.length
        ? settings.answers.map((a) => a.value).join(", ")
        : "미등록";
    }
    return "미등록";
  };

  return (
    <aside className="answer-review-panel" aria-label="정답 검수">
      <div className="review-tabs">
        <button type="button" aria-pressed={!editing} onClick={() => setEditing(false)}>
          풀어보기 및 빠른 정답 지정
        </button>
        <button type="button" aria-pressed={editing} onClick={() => setEditing(true)}>
          상세 설정
        </button>
      </div>

      <div className="review-status-header">
        <span className={`review-status-badge ${settings.status}`}>
          {{ pending: "미검수", needs_changes: "수정 필요", verified: "검수 완료" }[settings.status]}
        </span>
        {feedback ? <span className="review-feedback">{feedback}</span> : null}
      </div>

      {!hasAnswers && (
        <div className="review-alert-unverified">
          <strong>⚠️ 정답 미확인</strong>
          <p>등록된 정답이 없습니다. 아래에서 정답을 바로 입력하거나 지정하여 저장하세요.</p>
        </div>
      )}

      {editing ? (
        <>
          <label>
            응답 방식
            <select
              value={settings.mode}
              onChange={(event) => update({ mode: event.target.value as AnswerReviewSettings["mode"] })}
            >
              <option value="choice">선택형 (객관식 1~5번)</option>
              <option value="panel_input">직접 입력 (주관식 단답형)</option>
              <option value="ox">항목별 OX</option>
              <option value="grouped_choice">여러 소문항 선택형</option>
              <option value="canvas_slots">그림의 입력칸</option>
            </select>
          </label>
          <p className="review-help">
            보기가 있는 문제는 선택형, 여러 OX는 항목별 OX로 설정하세요. 내용이 모호하면 검수 보류 사유를 남겨 주세요.
          </p>

          {groupMode ? (
            <>
              {groups.map((group, index) => (
                <fieldset key={group.id}>
                  <legend>소문항 {index + 1}</legend>
                  <input
                    aria-label={`소문항 ${index + 1} 질문`}
                    value={group.label}
                    onChange={(event) =>
                      update({
                        groups: groups.map((g, i) => (i === index ? { ...g, label: event.target.value } : g)),
                      })
                    }
                  />
                  <label>
                    선택지 (한 줄에 하나)
                    <textarea
                      value={group.choices.join("\n")}
                      onChange={(event) =>
                        update({
                          groups: groups.map((g, i) =>
                            i === index ? { ...g, choices: event.target.value.split("\n"), correct_index: -1 } : g,
                          ),
                        })
                      }
                    />
                  </label>
                  <label>
                    정답
                    <select
                      value={group.correct_index}
                      onChange={(event) =>
                        update({
                          groups: groups.map((g, i) =>
                            i === index ? { ...g, correct_index: Number(event.target.value) } : g,
                          ),
                        })
                      }
                    >
                      <option value={-1}>정답 선택</option>
                      {group.choices.map((text, i) => (
                        <option key={i} value={i}>
                          {text}
                        </option>
                      ))}
                    </select>
                  </label>
                  <button type="button" onClick={() => update({ groups: groups.filter((_, i) => i !== index) })}>
                    소문항 삭제
                  </button>
                </fieldset>
              ))}
              <button
                type="button"
                onClick={() =>
                  update({
                    groups: [
                      ...groups,
                      { id: `group.${crypto.randomUUID()}`, label: `문항 ${groups.length + 1}`, choices: ["", ""], correct_index: -1 },
                    ],
                  })
                }
              >
                소문항 추가
              </button>
            </>
          ) : choiceMode ? (
            <>
              {settings.choices.map((choice, index) => (
                <fieldset key={choice.id}>
                  <legend>선택지 {index + 1}</legend>
                  <input
                    aria-label={`선택지 ${index + 1} 번호`}
                    value={choice.label}
                    onChange={(event) =>
                      update({
                        choices: settings.choices.map((item, i) =>
                          i === index ? { ...item, label: event.target.value } : item,
                        ),
                      })
                    }
                  />
                  <textarea
                    aria-label={`선택지 ${index + 1} 내용`}
                    value={choice.text}
                    onChange={(event) =>
                      update({
                        choices: settings.choices.map((item, i) =>
                          i === index ? { ...item, text: event.target.value } : item,
                        ),
                      })
                    }
                  />
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={choice.correct}
                      onChange={(event) =>
                        update({
                          choices: settings.choices.map((item, i) =>
                            i === index ? { ...item, correct: event.target.checked } : item,
                          ),
                        })
                      }
                    />{" "}
                    정답
                  </label>
                  <div className="review-tabs">
                    <button
                      type="button"
                      disabled={!choice.sourceRefs?.length}
                      onClick={() => onSelect(choice.sourceRefs ?? [])}
                    >
                      원본 선택
                    </button>
                    <button
                      type="button"
                      onClick={() => update({ choices: settings.choices.filter((_, i) => i !== index) })}
                    >
                      삭제
                    </button>
                  </div>
                </fieldset>
              ))}
              <button
                type="button"
                onClick={() =>
                  update({
                    choices: [
                      ...settings.choices,
                      { id: `choice.review.${crypto.randomUUID()}`, label: String(settings.choices.length + 1), text: "", correct: false },
                    ],
                  })
                }
              >
                선택지 추가
              </button>
              {expected.length > 1 && <p>복수 선택 문항입니다. 선택한 정답을 모두 골라야 정답으로 처리합니다.</p>}
            </>
          ) : (
            <>
              {settings.answers.map((answer, index) => (
                <div className="review-answer-row" key={index}>
                  <label>
                    답 {index + 1}
                    {settings.mode === "ox" ? (
                      <select
                        value={answer.value}
                        onChange={(event) =>
                          update({
                            answers: settings.answers.map((item, i) =>
                              i === index ? { ...item, value: event.target.value } : item,
                            ),
                          })
                        }
                      >
                        <option value="">선택</option>
                        <option value="O">O</option>
                        <option value="X">X</option>
                      </select>
                    ) : (
                      <input
                        value={answer.value}
                        onChange={(event) =>
                          update({
                            answers: settings.answers.map((item, i) =>
                              i === index ? { ...item, value: event.target.value } : item,
                            ),
                          })
                        }
                      />
                    )}
                  </label>
                  <button type="button" onClick={() => update({ answers: settings.answers.filter((_, i) => i !== index) })}>
                    삭제
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={() => update({ answers: [...settings.answers, { value: settings.mode === "ox" ? "O" : "" }] })}
              >
                답 항목 추가
              </button>
            </>
          )}

          <label>
            검수 상태
            <select
              value={settings.status}
              onChange={(event) => update({ status: event.target.value as AnswerReviewSettings["status"] })}
            >
              <option value="pending">미검수</option>
              <option value="needs_changes">수정 필요</option>
              <option value="verified">검수 완료</option>
            </select>
          </label>
          <label>
            검수 메모
            <textarea
              value={settings.note}
              onChange={(event) => update({ note: event.target.value })}
              placeholder="문항의 모호함, 정답 오류, 그림 수정 사항"
            />
          </label>
          <button type="button" onClick={onEditLayout}>
            지문·그림·여백 편집
          </button>
          <button
            type="button"
            className="btn-primary-register"
            disabled={busy || (settings.status === "verified" && !hasAnswers)}
            onClick={() => onSave()}
          >
            {busy ? "저장 중…" : "검수 저장 및 Build"}
          </button>
        </>
      ) : (
        <>
          {hasAnswers && (
            <div className="registered-answer-card">
              <div className="registered-answer-row">
                <span className="registered-label">현재 등록 정답:</span>
                <strong className="registered-value">{registeredAnswerSummary()}</strong>
              </div>
            </div>
          )}

          <div className="solve-section">
            <strong className="solve-prompt">
              {groupMode
                ? "각 소문항의 답을 선택하세요"
                : choiceMode
                  ? expected.length > 1
                    ? "맞는 답을 모두 선택하세요"
                    : "알맞은 답을 선택하세요"
                  : oxMode
                    ? "각 항목의 O 또는 X를 선택하세요"
                    : "정답을 입력하세요"}
            </strong>

            {groupMode ? (
              <>
                {groups.map((group, index) => (
                  <fieldset key={group.id} className="review-group-box">
                    <legend>{group.label}</legend>
                    {group.choices.map((text, i) => (
                      <label className="answer-review-choice" key={i}>
                        <input
                          type="radio"
                          name={`review-group-${index}`}
                          checked={responses[index] === String(i)}
                          onChange={() => {
                            setResult(null);
                            setResponses((values) => groups.map((_, n) => (n === index ? String(i) : values[n] ?? "")));
                          }}
                        />
                        <span>{text}</span>
                        {group.correct_index === i ? <span className="choice-correct-badge">✓ 등록 정답</span> : null}
                      </label>
                    ))}
                  </fieldset>
                ))}
                <div className="review-actions-column">
                  <button
                    type="button"
                    className="btn-register-action"
                    disabled={busy || groups.some((_, i) => responses[i] === undefined || responses[i] === "")}
                    onClick={registerGroupChoicesAndSave}
                  >
                    선택한 보기를 정답으로 등록 및 저장
                  </button>
                  <button
                    type="button"
                    disabled={!hasAnswers || groups.some((_, i) => !responses[i]?.trim())}
                    onClick={check}
                  >
                    정답 확인 (채점 테스트)
                  </button>
                </div>
              </>
            ) : choiceMode ? (
              <>
                <div className="answer-review-choices-list">
                  {settings.choices.map((choice) => (
                    <div key={choice.id} className={`review-choice-item${choice.correct ? " is-correct" : ""}`}>
                      <label className="answer-review-choice">
                        <input
                          type={expected.length > 1 ? "checkbox" : "radio"}
                          name="review-choice"
                          checked={selected.includes(choice.id)}
                          onChange={() => {
                            setResult(null);
                            setSelected(
                              expected.length > 1
                                ? selected.includes(choice.id)
                                  ? selected.filter((id) => id !== choice.id)
                                  : [...selected, choice.id]
                                : [choice.id],
                            );
                          }}
                        />
                        <span className="choice-marker">{choice.label}</span>
                        <span className="choice-text">{choice.text}</span>
                      </label>
                      <div className="choice-actions">
                        {choice.correct ? (
                          <span className="choice-correct-badge">✓ 정답</span>
                        ) : (
                          <button
                            type="button"
                            className="btn-set-answer-quick"
                            disabled={busy}
                            onClick={() => setChoiceAsCorrectAndSave(choice.id)}
                            title="이 보기를 정답으로 지정하고 즉시 저장 및 Build합니다"
                          >
                            정답으로 지정
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                <div className="review-actions-column">
                  {selected.length > 0 && (
                    <button
                      type="button"
                      className="btn-register-action"
                      disabled={busy}
                      onClick={setSelectedChoicesAsCorrectAndSave}
                    >
                      선택한 보기 ({selected.map((id) => settings.choices.find((c) => c.id === id)?.label).join(", ")})를 정답으로 등록 및 저장
                    </button>
                  )}
                  <button
                    type="button"
                    disabled={!hasAnswers || !selected.length}
                    onClick={check}
                  >
                    정답 확인 (채점 테스트)
                  </button>
                </div>
              </>
            ) : oxMode ? (
              <>
                <div className="ox-inputs-list">
                  {settings.answers.length > 0
                    ? settings.answers.map((_, index) => (
                        <label key={index} className="ox-input-item">
                          항목 {index + 1}
                          <select
                            value={responses[index] ?? ""}
                            onChange={(event) => {
                              setResult(null);
                              setResponses((values) =>
                                settings.answers.map((_, i) => (i === index ? event.target.value : values[i] ?? "")),
                              );
                            }}
                          >
                            <option value="">선택</option>
                            <option value="O">O</option>
                            <option value="X">X</option>
                          </select>
                        </label>
                      ))
                    : [0, 1, 2].map((index) => (
                        <label key={index} className="ox-input-item">
                          항목 {index + 1}
                          <select
                            value={responses[index] ?? ""}
                            onChange={(event) => {
                              setResult(null);
                              const copy = [...responses];
                              copy[index] = event.target.value;
                              setResponses(copy);
                            }}
                          >
                            <option value="">선택</option>
                            <option value="O">O</option>
                            <option value="X">X</option>
                          </select>
                        </label>
                      ))}
                </div>

                <div className="review-actions-column">
                  <button
                    type="button"
                    className="btn-register-action"
                    disabled={busy || responses.length === 0 || responses.some((r) => !/^[OX]$/.test(r))}
                    onClick={registerOxAnswersAndSave}
                  >
                    선택한 O/X를 정답으로 등록 및 저장
                  </button>
                  <button
                    type="button"
                    disabled={!hasAnswers || responses.length === 0 || responses.some((r) => !r)}
                    onClick={check}
                  >
                    정답 확인 (채점 테스트)
                  </button>
                </div>
              </>
            ) : (
              <>
                {/* panel_input or canvas_slots */}
                {!hasAnswers ? (
                  <div className="direct-answer-input-box">
                    <label>
                      새 정답 값 입력:
                      <input
                        type="text"
                        placeholder="정답 입력 (예: 25)"
                        value={customInputAnswer}
                        onChange={(e) => setCustomInputAnswer(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" && customInputAnswer.trim()) {
                            registerDirectInputAnswerAndSave(customInputAnswer);
                          }
                        }}
                      />
                    </label>
                    <button
                      type="button"
                      className="btn-register-action"
                      disabled={busy || !customInputAnswer.trim()}
                      onClick={() => registerDirectInputAnswerAndSave(customInputAnswer)}
                    >
                      입력한 값을 정답으로 등록 및 저장
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="edit-answer-toggle-row">
                      <button
                        type="button"
                        className="btn-link"
                        onClick={() => setShowInputEdit(!showInputEdit)}
                      >
                        {showInputEdit ? "정답 수정 닫기" : "다른 정답으로 직접 변경하기"}
                      </button>
                    </div>
                    {showInputEdit && (
                      <div className="direct-answer-input-box">
                        <label>
                          새 정답 값:
                          <input
                            type="text"
                            placeholder="새 정답 입력"
                            value={customInputAnswer}
                            onChange={(e) => setCustomInputAnswer(e.target.value)}
                          />
                        </label>
                        <button
                          type="button"
                          className="btn-register-action"
                          disabled={busy || !customInputAnswer.trim()}
                          onClick={() => registerDirectInputAnswerAndSave(customInputAnswer)}
                        >
                          새 정답으로 수정 및 저장
                        </button>
                      </div>
                    )}
                  </>
                )}

                <div className="test-solve-box">
                  <label>
                    정답 확인 테스트 (학생 답안):
                    <input
                      value={responses[0] ?? ""}
                      placeholder="답안을 입력해 보세요"
                      onChange={(event) => {
                        setResult(null);
                        setResponses([event.target.value]);
                      }}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && hasAnswers && responses[0]?.trim()) {
                          check();
                        }
                      }}
                      autoComplete="off"
                    />
                  </label>
                  <button
                    type="button"
                    disabled={!hasAnswers || !responses[0]?.trim()}
                    onClick={check}
                  >
                    정답 확인
                  </button>
                </div>
              </>
            )}

            {result && (
              <p
                role="status"
                className={`review-result-msg ${result.startsWith("✓") ? "success" : "failure"}`}
              >
                {result}
              </p>
            )}
            <p className="review-help">
              등록된 정답과 비교하는 검수용 채점입니다. 문항과 풀이의 타당성도 함께 확인해 주세요.
            </p>
          </div>
        </>
      )}
    </aside>
  );
}
