import { useState } from "react";

export default function ImaUI() {
  const [messages, setMessages] = useState([
    { role: "ima", text: "אני כאן איתך. מה אתה רוצה ליצור היום?" }
  ]);

  const [input, setInput] = useState("");

  const send = async () => {
    if (!input) return;

    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);

    setInput("");

import API_BASE from "./config";

fetch(`${API_BASE}/ima/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();

    setMessages(prev => [
      ...prev,
      { role: "ima", text: data.result }
    ]);
  };

  return (
    <div style={{ background: "#000", color: "#fff", height: "100vh", display: "flex", flexDirection: "column" }}>
      <div style={{ padding: 16, borderBottom: "1px solid #333" }}>
        IMA — Adaptive System
      </div>

      <div style={{ flex: 1, padding: 16, overflow: "auto" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ textAlign: m.role === "user" ? "right" : "left", margin: "8px 0" }}>
            <span style={{ padding: 10, background: "#111", borderRadius: 10, display: "inline-block" }}>
              {m.text}
            </span>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", padding: 10, borderTop: "1px solid #333" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ flex: 1, padding: 10 }}
        />
        <button onClick={send} style={{ marginLeft: 10 }}>
          שלח
        </button>
      </div>
    </div>
  );
}
