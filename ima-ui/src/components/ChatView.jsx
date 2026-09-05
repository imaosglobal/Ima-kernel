import { useState, useRef, useEffect } from "react";
import { useI18n } from "../i18n/I18nProvider";
import { askIMA } from "../api/imaClient";
import IMAAvatar from "./IMAAvatar";
import "./ChatView.css";

function formatMessage(text) {
  return text.split("\n").map((line, i) => (
    <span key={i}>
      {line}
      {i < text.split("\n").length - 1 && <br />}
    </span>
  ));
}

export default function ChatView({ initialMessage, onClearInitial, user }) {
  const { t, lang } = useI18n();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copiedId, setCopiedId] = useState(null);
  const scrollRef = useRef(null);
  const sentInitial = useRef(false);

  async function sendMessage(text) {
    const userMsg = { id: Date.now(), role: "user", text };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const r = await askIMA(text, lang);
      const responseText =
        r.answer?.response || r.response || JSON.stringify(r);
      setMessages((m) => [
        ...m,
        { id: Date.now() + 1, role: "ima", text: responseText },
      ]);
    } catch (e) {
      setError(t("chat.error"));
    } finally {
      setLoading(false);
    }
  }

  // Handle initial message from landing
  useEffect(() => {
    if (initialMessage && !sentInitial.current) {
      sentInitial.current = true;
      sendMessage(initialMessage);
      onClearInitial();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialMessage]);

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim() || loading) return;
    sendMessage(input.trim());
  }

  function handleCopy(id, text) {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  }

  function handleClearChat() {
    setMessages([]);
    setError(null);
  }

  return (
    <div className="chat-view">
      <div className="chat-messages" ref={scrollRef}>
        {messages.length === 0 && !loading && (
          <div className="chat-empty">
            <IMAAvatar variant={user?.avatar || "aura"} size="md" />
            <p>{t("chat.emptyState")}</p>
          </div>
        )}

        {messages.map((m) => (
          <div key={m.id} className={`chat-msg chat-msg-${m.role}`}>
            <div className="chat-msg-bubble">
              {formatMessage(m.text)}
            </div>
            {m.role === "ima" && (
              <div className="chat-msg-actions">
                <button
                  className="chat-msg-action"
                  onClick={() => handleCopy(m.id, m.text)}
                >
                  {copiedId === m.id ? t("chat.copied") : t("chat.copy")}
                </button>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="chat-msg chat-msg-ima">
            <div className="chat-msg-bubble chat-thinking">
              <span className="chat-dot-anim" />
              <span className="chat-dot-anim" />
              <span className="chat-dot-anim" />
            </div>
          </div>
        )}

        {error && (
          <div className="chat-error-msg">
            {error}
            <button className="chat-retry" onClick={() => setError(null)}>
              ✕
            </button>
          </div>
        )}
      </div>

      <div className="chat-toolbar">
        {messages.length > 0 && (
          <button className="chat-clear-btn" onClick={handleClearChat}>
            {t("chat.clearChat")}
          </button>
        )}
      </div>

      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <button
          className="chat-voice-btn"
          disabled
          title={t("chat.comingSoon")}
        >
          <span className="chat-voice-icon" />
        </button>
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t("chat.placeholder")}
          disabled={loading}
        />
        <button
          type="submit"
          className="chat-send-btn"
          disabled={!input.trim() || loading}
        >
          <span className="chat-send-icon" />
        </button>
      </form>
    </div>
  );
}
