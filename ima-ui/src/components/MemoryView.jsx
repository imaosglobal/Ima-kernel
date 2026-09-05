import { useI18n } from "../i18n/I18nProvider";
import "./MemoryView.css";

export default function MemoryView({ user, removeMemory, clearMemory, clearConversations }) {
  const { t } = useI18n();

  const conversations = user.conversations || [];
  const memories = user.memory || [];

  return (
    <div className="memory-view">
      {/* Conversations */}
      <div className="memory-section">
        <div className="memory-section-head">
          <span className="memory-section-label">{t("memory.conversations")}</span>
          {conversations.length > 0 && (
            <button className="memory-clear-btn" onClick={clearConversations}>
              {t("chat.clearChat")}
            </button>
          )}
        </div>
        {conversations.length === 0 ? (
          <p className="memory-empty-text">{t("memory.noConversations")}</p>
        ) : (
          <div className="memory-list">
            {conversations.map((c, i) => (
              <div key={i} className="memory-item">
                <div className="memory-item-q">{c.in || c.question || ""}</div>
                <div className="memory-item-a">{c.out || c.response || ""}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Saved facts */}
      <div className="memory-section">
        <div className="memory-section-head">
          <span className="memory-section-label">{t("memory.facts")}</span>
          {memories.length > 0 && (
            <button
              className="memory-clear-btn"
              onClick={() => {
                if (confirm(t("memory.clearConfirm"))) clearMemory();
              }}
            >
              {t("memory.clearAll")}
            </button>
          )}
        </div>
        {memories.length === 0 ? (
          <p className="memory-empty-text">{t("memory.empty")}</p>
        ) : (
          <div className="memory-list">
            {memories.map((m) => (
              <div key={m.id} className="memory-fact-item">
                <span className="memory-fact-text">{m.text || m.fact || ""}</span>
                <button
                  className="memory-forget-btn"
                  onClick={() => removeMemory(m.id)}
                >
                  {t("memory.forget")}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
