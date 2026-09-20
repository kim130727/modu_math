import React, { useEffect, useState } from "react";
import { renderWatercolorAvatar, watercolorKey } from "./watercolorRenderer";
import {
  ACCESSORY_OPTIONS,
  type AvatarAccessory,
  type AvatarConfig,
  type AvatarEyes,
  type AvatarGender,
  type AvatarHairStyle,
  type AvatarMouth,
  type AvatarPose,
  BOY_HAIR_OPTIONS,
  CLOTH_COLOR_PALETTES,
  EYES_OPTIONS,
  GIRL_HAIR_OPTIONS,
  HAIR_COLOR_PALETTES,
  MOUTH_OPTIONS,
  POSE_OPTIONS,
  SKIN_TONE_PALETTES,
  generateRandomAvatarConfig,
  getDefaultAvatarConfig,
} from "./avatarParts";

interface KidAvatarMakerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onInsertAvatar: (config: AvatarConfig, svgDataUrl: string) => void;
  replacementTargets: { id: string; label: string }[];
  replacementTargetId: string;
  onReplacementTargetChange: (id: string) => void;
}

type TabType = "hair" | "face" | "pose" | "accessory" | "speech";

export const KidAvatarMakerModal: React.FC<KidAvatarMakerModalProps> = ({
  isOpen,
  onClose,
  onInsertAvatar,
  replacementTargets,
  replacementTargetId,
  onReplacementTargetChange,
}) => {
  const [config, setConfig] = useState<AvatarConfig>(() => getDefaultAvatarConfig("boy"));
  const [activeTab, setActiveTab] = useState<TabType>("hair");
  const [inserting, setInserting] = useState(false);
  const [error, setError] = useState("");

  const [retry, setRetry] = useState(0);
  const preview = useWatercolorPreview(config, isOpen, retry);

  if (!isOpen) return null;

  const handleGenderChange = (gender: AvatarGender) => {
    setConfig((prev) => ({
      ...prev,
      gender,
      hair: getDefaultAvatarConfig(gender).hair,
      eyes: getDefaultAvatarConfig(gender).eyes,
    }));
  };

  const handleRandomize = () => {
    setConfig(generateRandomAvatarConfig(config.gender));
  };

  const handleInsert = async () => {
    if (inserting || !preview.src || preview.busy) return;
    setInserting(true);
    setError("");
    try {
      onInsertAvatar(config, preview.src);
      onClose();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "캐릭터 삽입에 실패했습니다.");
    } finally {
      setInserting(false);
    }
  };

  const currentHairList = config.gender === "boy" ? BOY_HAIR_OPTIONS : GIRL_HAIR_OPTIONS;

  return (
    <div className="avatar-modal-overlay" onClick={() => { if (!inserting) onClose(); }}>
      <div className="avatar-modal-container" role="dialog" aria-modal="true" aria-label="캐릭터 만들기" aria-busy={inserting} onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="avatar-modal-header">
          <div className="avatar-modal-title">
            <span className="avatar-modal-icon">🧒</span>
            <span>캐릭터 만들기</span>
            <span className="avatar-modal-badge">수채화 일러스트</span>
          </div>
          <button className="avatar-modal-close" disabled={inserting} onClick={onClose} title="닫기">
            ✕
          </button>
        </div>

        {/* Body Content */}
        <div className="avatar-modal-body">
          {/* Left Column: Live Preview & Tone Selectors */}
          <div className="avatar-preview-column">
            <div className="avatar-preview-card">
              <div className="avatar-preview-box avatar-watercolor-preview" aria-busy={preview.busy}>
                {preview.src ? <img src={preview.src} alt="선택한 설정의 수채화 캐릭터" className="avatar-preview-image" /> : <span role="status">{preview.error ? "그림을 불러오지 못했습니다" : "수채화 캐릭터 준비 중…"}</span>}
                {config.hasSpeechBubble && config.speechText ? (
                  <div className="avatar-preview-bubble">
                    <span>{config.speechText}</span>
                  </div>
                ) : null}
              </div>


              {/* Gender Toggle */}
              <div className="avatar-gender-toggle">
                <button
                  className={`avatar-gender-btn ${config.gender === "boy" ? "active" : ""}`}
                  onClick={() => handleGenderChange("boy")}
                >
                  👦 남아 (Boy)
                </button>
                <button
                  className={`avatar-gender-btn ${config.gender === "girl" ? "active" : ""}`}
                  onClick={() => handleGenderChange("girl")}
                >
                  👧 여아 (Girl)
                </button>
              </div>

              {/* Skin Tone Selector (Global Diversity) */}
              <div className="avatar-color-section">
                <div className="avatar-section-label">🌍 글로벌 피부톤 (Skin Tone)</div>
                <div className="avatar-color-palette-6">
                  {SKIN_TONE_PALETTES.map((s) => (
                    <button
                      key={s.color}
                      className={`avatar-color-swatch ${config.skinTone === s.color ? "active" : ""}`}
                      style={{ backgroundColor: s.color }}
                      onClick={() => setConfig((prev) => ({ ...prev, skinTone: s.color }))}
                      title={s.name}
                    />
                  ))}
                </div>
              </div>

              {/* Hair Color Selector */}
              <div className="avatar-color-section">
                <div className="avatar-section-label">💇 헤어 색상 (Hair Color)</div>
                <div className="avatar-color-palette-6">
                  {HAIR_COLOR_PALETTES.map((h) => (
                    <button
                      key={h.color}
                      className={`avatar-color-swatch ${config.hairColor === h.color ? "active" : ""}`}
                      style={{ backgroundColor: h.color }}
                      onClick={() => setConfig((prev) => ({ ...prev, hairColor: h.color }))}
                      title={h.name}
                    />
                  ))}
                </div>
              </div>

              {/* Cloth Color Palette */}
              <div className="avatar-color-section">
                <div className="avatar-section-label">👕 옷 포인트 색상</div>
                <div className="avatar-color-palette">
                  {CLOTH_COLOR_PALETTES.map((p) => (
                    <button
                      key={p.color}
                      className={`avatar-color-swatch ${config.clothColor === p.color ? "active" : ""}`}
                      style={{ backgroundColor: p.color }}
                      onClick={() => setConfig((prev) => ({ ...prev, clothColor: p.color }))}
                      title={p.name}
                    />
                  ))}
                </div>
              </div>

              {/* Random Button */}
              <button className="avatar-random-btn" onClick={handleRandomize}>
                🎲 랜덤 캐릭터 생성
              </button>
            </div>
          </div>

          {/* Right Column: Customization Tabs & Options */}
          <div className="avatar-control-column">
            {/* Category Tabs */}
            <div className="avatar-tabs-nav">

              <button
                className={`avatar-tab-btn ${activeTab === "hair" ? "active" : ""}`}
                onClick={() => setActiveTab("hair")}
              >
                헤어스타일
              </button>
              <button
                className={`avatar-tab-btn ${activeTab === "face" ? "active" : ""}`}
                onClick={() => setActiveTab("face")}
              >
                표정 (눈/입)
              </button>
              <button
                className={`avatar-tab-btn ${activeTab === "pose" ? "active" : ""}`}
                onClick={() => setActiveTab("pose")}
              >
                동작 & 포즈
              </button>
              <button
                className={`avatar-tab-btn ${activeTab === "accessory" ? "active" : ""}`}
                onClick={() => setActiveTab("accessory")}
              >
                소품 & 안경
              </button>
              <button
                className={`avatar-tab-btn ${activeTab === "speech" ? "active" : ""}`}
                onClick={() => setActiveTab("speech")}
              >
                💬 말풍선
              </button>
            </div>

            {/* Tab Contents */}
            <div className="avatar-tab-content">
              {/* Tab: Hair */}
              {activeTab === "hair" && (
                <div className="avatar-options-grid">
                  {currentHairList.map((item) => (
                    <button
                      key={item.id}
                      className={`avatar-option-card ${config.hair === item.id ? "selected" : ""}`}
                      onClick={() => setConfig((prev) => ({ ...prev, hair: item.id }))}
                    >
                      <div className="avatar-option-preview">
                        <WatercolorThumbnail config={{ ...config, hair: item.id }} label={item.label} />
                      </div>
                      <div className="avatar-option-label">{item.label}</div>
                    </button>
                  ))}
                </div>
              )}

              {/* Tab: Face (Eyes & Mouth) */}
              {activeTab === "face" && (
                <div className="avatar-options-sections">
                  <div className="avatar-subsection">
                    <div className="avatar-subsection-title">👀 눈 & 눈썹 모양</div>
                    <div className="avatar-chips-row">
                      {EYES_OPTIONS.map((item) => (
                        <button
                          key={item.id}
                          className={`avatar-chip-btn ${config.eyes === item.id ? "selected" : ""}`}
                          onClick={() => setConfig((prev) => ({ ...prev, eyes: item.id }))}
                        >
                          {item.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="avatar-subsection">
                    <div className="avatar-subsection-title">👄 입 모양 & 표정</div>
                    <div className="avatar-chips-row">
                      {MOUTH_OPTIONS.map((item) => (
                        <button
                          key={item.id}
                          className={`avatar-chip-btn ${config.mouth === item.id ? "selected" : ""}`}
                          onClick={() => setConfig((prev) => ({ ...prev, mouth: item.id }))}
                        >
                          {item.label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Tab: Pose */}
              {activeTab === "pose" && (
                <div className="avatar-options-grid">
                  {POSE_OPTIONS.map((item) => (
                    <button
                      key={item.id}
                      className={`avatar-option-card ${config.pose === item.id ? "selected" : ""}`}
                      onClick={() => setConfig((prev) => ({ ...prev, pose: item.id }))}
                    >
                      <div className="avatar-option-preview">
                        <WatercolorThumbnail config={{ ...config, pose: item.id }} label={item.label} />
                      </div>
                      <div className="avatar-option-label">{item.label}</div>
                    </button>
                  ))}
                </div>
              )}

              {/* Tab: Accessory */}
              {activeTab === "accessory" && (
                <div className="avatar-options-grid">
                  {ACCESSORY_OPTIONS.map((item) => (
                    <button
                      key={item.id}
                      className={`avatar-option-card ${config.accessory === item.id ? "selected" : ""}`}
                      onClick={() => setConfig((prev) => ({ ...prev, accessory: item.id }))}
                    >
                      <div className="avatar-option-preview">
                        <WatercolorThumbnail config={{ ...config, accessory: item.id }} label={item.label} />
                      </div>
                      <div className="avatar-option-label">{item.label}</div>
                    </button>
                  ))}
                </div>
              )}

              {/* Tab: Speech Bubble */}
              {activeTab === "speech" && (
                <div className="avatar-speech-settings">
                  <label className="avatar-checkbox-row">
                    <input
                      type="checkbox"
                      checked={config.hasSpeechBubble ?? false}
                      onChange={(e) =>
                        setConfig((prev) => ({ ...prev, hasSpeechBubble: e.target.checked }))
                      }
                    />
                    <span className="avatar-checkbox-label">
                      캐릭터 옆에 말풍선 함께 삽입하기 (1-Click)
                    </span>
                  </label>

                  {config.hasSpeechBubble && (
                    <div className="avatar-speech-inputs">
                      <div className="avatar-input-group">
                        <label className="avatar-input-label">말풍선 대사 입력:</label>
                        <input
                          type="text"
                          className="avatar-text-input"
                          value={config.speechText ?? ""}
                          placeholder="예: 문제를 꼼꼼하게 읽어보자!"
                          onChange={(e) =>
                            setConfig((prev) => ({ ...prev, speechText: e.target.value }))
                          }
                          maxLength={40}
                        />
                      </div>

                      <div className="avatar-input-group">
                        <label className="avatar-input-label">말풍선 위치:</label>
                        <div className="avatar-bubble-pos-row">
                          <button
                            className={`avatar-chip-btn ${config.bubblePosition === "top-right" ? "selected" : ""}`}
                            onClick={() =>
                              setConfig((prev) => ({ ...prev, bubblePosition: "top-right" }))
                            }
                          >
                            우측 상단 ↗
                          </button>
                          <button
                            className={`avatar-chip-btn ${config.bubblePosition === "right" ? "selected" : ""}`}
                            onClick={() =>
                              setConfig((prev) => ({ ...prev, bubblePosition: "right" }))
                            }
                          >
                            우측 중앙 →
                          </button>
                          <button
                            className={`avatar-chip-btn ${config.bubblePosition === "top-left" ? "selected" : ""}`}
                            onClick={() =>
                              setConfig((prev) => ({ ...prev, bubblePosition: "top-left" }))
                            }
                          >
                            좌측 상단 ↖
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="avatar-modal-footer">
          <div className="avatar-footer-hint">
            {(error || preview.error) && <p role="alert" className="avatar-insert-error">{error || preview.error} <button onClick={() => setRetry((value) => value + 1)}>다시 불러오기</button></p>}
            <label>
              삽입 방식{" "}
              <select value={replacementTargetId} onChange={(event) => onReplacementTargetChange(event.target.value)}>
                <option value="">새 캐릭터 추가</option>
                {replacementTargets.map((target) => <option key={target.id} value={target.id}>{target.label} 교체</option>)}
              </select>
            </label>
            <div>{replacementTargetId ? "기존 위치와 크기로 교체하며 이름과 말풍선은 유지합니다." : "기존 캐릭터를 바꾸려면 교체 대상을 선택하세요."}</div>
          </div>
          <div className="avatar-footer-actions">
            <button className="avatar-btn-cancel" disabled={inserting} onClick={onClose}>
              취소
            </button>
            <button className="avatar-btn-insert" disabled={inserting || preview.busy || !preview.src} onClick={handleInsert}>
              {inserting || preview.busy ? "이미지 준비 중…" : replacementTargetId ? "✨ 선택한 캐릭터 교체" : "✨ 캔버스에 삽입"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

function useWatercolorPreview(config: AvatarConfig, enabled = true, retry = 0) {
  const key = watercolorKey(config);
  const [result, setResult] = useState({ key: "", src: "", error: "" });
  useEffect(() => {
    if (!enabled) return;
    let active = true;
    setResult({ key: "", src: "", error: "" });
    const timer = setTimeout(() => {
      renderWatercolorAvatar(config).then(
        (src) => { if (active) setResult({ key, src, error: "" }); },
        (cause) => { if (active) setResult({ key, src: "", error: cause instanceof Error ? cause.message : "이미지를 준비하지 못했습니다." }); },
      );
    }, 40);
    return () => { active = false; clearTimeout(timer); };
  }, [key, enabled, retry]);
  return result.key === key ? { ...result, busy: false } : { src: "", error: "", busy: enabled };
}

function WatercolorThumbnail({ config, label }: { config: AvatarConfig; label: string }) {
  const preview = useWatercolorPreview(config);
  return preview.src
    ? <img src={preview.src} alt={label} className="avatar-mini-preview" />
    : <span aria-label={preview.error || "미리보기 준비 중"}>…</span>;
}
