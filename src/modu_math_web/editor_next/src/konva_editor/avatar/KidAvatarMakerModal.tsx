import React, { useMemo, useState } from "react";
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
  compileAvatarSvg,
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
}

type TabType = "hair" | "face" | "pose" | "accessory" | "speech";

export const KidAvatarMakerModal: React.FC<KidAvatarMakerModalProps> = ({
  isOpen,
  onClose,
  onInsertAvatar,
}) => {
  const [config, setConfig] = useState<AvatarConfig>(() => getDefaultAvatarConfig("boy"));
  const [activeTab, setActiveTab] = useState<TabType>("hair");

  const previewSvgUrl = useMemo(() => compileAvatarSvg(config), [config]);

  if (!isOpen) return null;

  const handleGenderChange = (gender: AvatarGender) => {
    setConfig((prev) => ({
      ...prev,
      gender,
      hair: gender === "boy" ? "boy_dandy" : "girl_twintail",
      eyes: gender === "boy" ? "smile" : "sparkle",
      clothColor: gender === "boy" ? "#6366f1" : "#f472b6",
    }));
  };

  const handleRandomize = () => {
    setConfig(generateRandomAvatarConfig(config.gender));
  };

  const handleInsert = () => {
    onInsertAvatar(config, previewSvgUrl);
    onClose();
  };

  const currentHairList = config.gender === "boy" ? BOY_HAIR_OPTIONS : GIRL_HAIR_OPTIONS;

  return (
    <div className="avatar-modal-overlay" onClick={onClose}>
      <div className="avatar-modal-container" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="avatar-modal-header">
          <div className="avatar-modal-title">
            <span className="avatar-modal-icon">🧒</span>
            <span>글로벌 어린이 아바타 만들기</span>
            <span className="avatar-modal-badge">초경량 벡터</span>
          </div>
          <button className="avatar-modal-close" onClick={onClose} title="닫기">
            ✕
          </button>
        </div>

        {/* Body Content */}
        <div className="avatar-modal-body">
          {/* Left Column: Live Preview & Tone Selectors */}
          <div className="avatar-preview-column">
            <div className="avatar-preview-card">
              <div className="avatar-preview-box">
                <img src={previewSvgUrl} alt="Avatar Preview" className="avatar-preview-image" />
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
                        <img
                          src={compileAvatarSvg({ ...config, hair: item.id })}
                          alt={item.label}
                          className="avatar-mini-preview"
                        />
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
                        <img
                          src={compileAvatarSvg({ ...config, pose: item.id })}
                          alt={item.label}
                          className="avatar-mini-preview"
                        />
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
                        <img
                          src={compileAvatarSvg({ ...config, accessory: item.id })}
                          alt={item.label}
                          className="avatar-mini-preview"
                        />
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
            💡 100% 자체 제작 독창적 벡터 그래픽으로 저작권 걱정 없이 자유롭게 사용하실 수 있습니다.
          </div>
          <div className="avatar-footer-actions">
            <button className="avatar-btn-cancel" onClick={onClose}>
              취소
            </button>
            <button className="avatar-btn-insert" onClick={handleInsert}>
              ✨ 캔버스에 삽입
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
