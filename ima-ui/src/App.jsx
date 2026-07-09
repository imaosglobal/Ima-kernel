import { useState } from "react";

export default function App() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState([]);
  const [state, setState] = useState("idle");

  const send = async () => {
    if (!input.trim()) return;

    const msg = input;
    setInput("");

    // הוספת הודעת משתמש לצ'אט
    setChat((prev) => [...prev, { role: "user", text: msg }]);

    setState("thinking");

    try {
      const res = await fetch("http://localhost:3000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg }),
      });

      const data = await res.json();

      setChat((prev) => [
        ...prev,
        { role: "ima", text: data.reply || "אין תשובה" },
      ]);
    } catch (e) {
      setChat((prev) => [
        ...prev,
        { role: "ima", text: "שגיאה בחיבור לשרת" },
      ]);
    }

    setState("idle");
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>IMA</h2>

      <div style={{ marginBottom: 10 }}>
        מצב: {state}
      </div>

      <div style={{
        border: "1px solid #ccc",
        padding: 10,
        height: 300,
        overflowY: "auto",
        marginBottom: 10
      }}>
        {chat.map((m, i) => (
          <div key={i}>
            <b>{m.role}:</b> {m.text}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="כתוב משהו..."
        style={{ width: "70%" }}
      />

      <button onClick={send} style={{ marginLeft: 10 }}>
        שלח
      </button>
    </div>
  );
}
