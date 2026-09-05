import { useI18n } from "../i18n/I18nProvider";
import { AVATAR_VARIANTS, AVATAR_LIST } from "./avatars";
import "./AvatarPicker.css";

export default function AvatarPicker({ value, onChange }) {
  const { lang } = useI18n();

  return (
    <div className="avatar-picker">
      <div className="avatar-picker-grid">
        {AVATAR_LIST.map((key) => {
          const v = AVATAR_VARIANTS[key];
          return (
            <button
              key={key}
              className={`avatar-picker-option ${value === key ? "avatar-picker-selected" : ""}`}
              onClick={() => onChange(key)}
            >
              <span
                className="avatar-picker-orb"
                style={{
                  background: `radial-gradient(circle at 35% 35%, ${v.from}, ${v.via} 50%, ${v.to} 100%)`,
                  boxShadow: `0 0 16px ${v.glow}`,
                }}
              />
              <span className="avatar-picker-label">{v.label[lang]}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
