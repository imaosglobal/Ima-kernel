import { useState } from "react";
import { askIma } from "../services/imaChat";
import Message from "./Message";

export default function Chat({ language = "he", user = null }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  async function send() {
    const value = String(input || "").trim();
    if (!value || busy) return;

    setInput("");
    setMessages((items) => [...items, { role: "user", text: value }]);
    setBusy(true);

    try {
      const response = await askIma(value, {
        language,
        interface: "public-chat-component",
        authenticated: Boolean(user),
        device_locale: navigator.language || language,
      });
      setMessages((items) => [...items, { role: "ima", text: response }]);
    } catch {
      setMessages((items) => [
        ...items,
        {
          role: "ima",
          text: language === "he"
            ? "אני לא יודעת עדיין את התשובה לשאלה הזו. אין לי כרגע מספיק מידע מאומת כדי לענות עליה בוודאות, ואני לא אמציא תשובה."
            : "I don't know the answer yet. I don't have enough verified information to answer with confidence, and I won't invent one.",
        },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="chat">
      <div className="messages" aria-live="polite">
        {messages.map((message, index) => (
          <Message key={index} {...message} />
        ))}
        {busy && <Message role="ima" text={language === "he" ? "אמא חושבת…" : "IMA is thinking…"} />}
      </div>

      <div className="input">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => event.key === "Enter" && send()}
          placeholder={language === "he" ? "דברי עם אמא…" : "Talk to IMA…"}
          aria-label={language === "he" ? "הודעה לאמא" : "Message IMA"}
        />
        <button onClick={send} disabled={busy || !input.trim()}>
          {language === "he" ? "שלח" : "Send"}
        </button>
      </div>
    </div>
  );
}
