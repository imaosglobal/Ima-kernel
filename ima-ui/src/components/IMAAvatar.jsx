import { AVATAR_VARIANTS } from "./avatars";
import "./IMAAvatar.css";

export default function IMAAvatar({ variant = "aura", size = "md" }) {
  const v = AVATAR_VARIANTS[variant] || AVATAR_VARIANTS.aura;

  return (
    <span
      className={`ima-avatar ima-avatar-${size}`}
      style={{
        background: `radial-gradient(circle at 35% 35%, ${v.from}, ${v.via} 50%, ${v.to} 100%)`,
        boxShadow: `0 0 ${size === "lg" ? 40 : size === "md" ? 20 : 12}px ${v.glow}, inset 0 0 20px rgba(255,255,255,0.1)`,
      }}
    >
      <span
        className="ima-avatar-shine"
        style={{ background: `radial-gradient(circle at 35% 30%, rgba(255,255,255,0.4), transparent 50%)` }}
      />
    </span>
  );
}
