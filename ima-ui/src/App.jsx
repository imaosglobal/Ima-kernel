import { useEffect, useState } from "react";
import Chat from "./components/Chat";
import MemoryPanel from "./components/MemoryPanel";
import IMAAvatar from "./components/avatar/IMAAvatar";
import { getHealth, getReady } from "./api/imaClient";
import "./App.css";

const NAV = [
  { id: "ima", label: "IMA" },
  { id: "memory", label: "זיכרון" },
  { id: "system", label: "מערכת" },
];

function StatusDot({ state }) {
  return <span className={`status-dot status-${state}`} aria-hidden="true" />;
}

function SystemStatus() {
  const [health, setHealth] = useState(null);
  const [ready, setReady] = useState(null);

  useEffect(() => {
    let alive = true;

    async function check() {
      try {
        const [h, r] = await Promise.all([
          getHealth(),
          getReady(),
        ]);

        if (alive) {
          setHealth(h);
          setReady(r);
        }
      } catch {
        if (alive) {
          setHealth(null);
          setReady(null);
        }
      }
    }

    check();

    const timer = setInterval(check, 15000);

    return () => {
      alive = false;
      clearInterval(timer);
    };
  }, []);

  const connected = Boolean(health);
  const operational = Boolean(ready);

  return (
    <div className="system-status">
      <div className="status-line">
        <StatusDot state={connected ? "online" : "offline"} />
        <span>{connected ? "הליבה מחוברת" : "הליבה לא זמינה"}</span>
      </div>

      <div className="status-line muted">
        <StatusDot state={operational ? "online" : "idle"} />
        <span>{operational ? "IMA מוכנה" : "בודקת מוכנות"}</span>
      </div>
    </div>
  );
}

function Capability({ label, detail }) {
  return (
    <div className="capability">
      <span className="capability-mark" />

      <div>
        <strong>{label}</strong>
        <span>{detail}</span>
      </div>
    </div>
  );
}

export default function App() {
  const [active, setActive] = useState("ima");
  const [mobilePanel, setMobilePanel] = useState(false);

  return (
    <main className="ima-app">

      <header className="topbar">

        <button
          className="brand"
          onClick={() => setActive("ima")}
          aria-label="IMA"
        >
          <span className="brand-orb" />

          <span className="brand-copy">
            <strong>IMA</strong>
            <small>PERSONAL INTELLIGENCE</small>
          </span>
        </button>

        <nav className="topnav" aria-label="ניווט ראשי">
          {NAV.map((item) => (
            <button
              key={item.id}
              className={active === item.id ? "nav-active" : ""}
              onClick={() => setActive(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>

        <div className="top-status">
          <StatusDot state="online" />
          <span>ONLINE</span>
        </div>

        <button
          className="mobile-toggle"
          onClick={() => setMobilePanel((value) => !value)}
          aria-label="פתיחת מידע"
          aria-expanded={mobilePanel}
        >
          +
        </button>

      </header>

      <div className="workspace">

        <aside className="left-rail">

          <div className="rail-label">
            IDENTITY
          </div>

          <div className="presence-card">

            <div className="presence-avatar">
              <IMAAvatar compact />
            </div>

            <div className="presence-copy">
              <strong>IMA</strong>
              <span>adaptive-human</span>
            </div>

            <div className="presence-state">
              <StatusDot state="online" />
              <span>נוכחת</span>
            </div>

          </div>

          <div className="rail-section">

            <div className="rail-label">
              CAPABILITIES
            </div>

            <Capability label="שיחה" detail="Connected" />
            <Capability label="זיכרון" detail="Local layer" />
            <Capability label="למידה" detail="Learning layer" />
            <Capability label="יצירה" detail="Available" />
            <Capability label="טכנולוגיה" detail="Available" />

          </div>

          <div className="rail-footer">
            <SystemStatus />
          </div>

        </aside>

        <section className="main-surface">

          {active === "ima" && (
            <>
              <div className="conversation-header">

                <div>
                  <span className="eyebrow">
                    PERSONAL INTELLIGENCE
                  </span>

                  <h1>
                    שיחה עם IMA
                  </h1>

                  <p>
                    מרחב אחד לשיחה, יצירה, חקירה ולמידה.
                  </p>
                </div>

                <div className="header-presence">
                  <span className="pulse" />
                  <span>IMA נוכחת</span>
                </div>

              </div>

              <div className="chat-shell">
                <Chat />
              </div>
            </>
          )}

          {active === "memory" && (
            <>
              <div className="conversation-header">

                <div>
                  <span className="eyebrow">
                    MEMORY LAYER
                  </span>

                  <h1>
                    זיכרון
                  </h1>

                  <p>
                    השכבה המקומית המחוברת לממשק IMA.
                  </p>
                </div>

              </div>

              <div className="content-card">
                <MemoryPanel />
              </div>
            </>
          )}

          {active === "system" && (
            <>
              <div className="conversation-header">

                <div>
                  <span className="eyebrow">
                    SYSTEM
                  </span>

                  <h1>
                    מצב המערכת
                  </h1>

                  <p>
                    מצב החיבור בפועל ל־IMA backend.
                  </p>
                </div>

              </div>

              <div className="system-grid">

                <div className="system-card">
                  <span className="eyebrow">API</span>

                  <h2>/ask</h2>

                  <p>
                    ערוץ השיחה הפעיל של IMA.
                  </p>

                  <div className="live-state">
                    <StatusDot state="online" />
                    פעיל
                  </div>
                </div>

                <div className="system-card">
                  <span className="eyebrow">HEALTH</span>

                  <h2>/health</h2>

                  <p>
                    בדיקת תקינות הליבה.
                  </p>

                  <SystemStatus />
                </div>

                <div className="system-card">
                  <span className="eyebrow">READY</span>

                  <h2>/ready</h2>

                  <p>
                    בדיקת מוכנות המערכת.
                  </p>

                  <SystemStatus />
                </div>

              </div>
            </>
          )}

        </section>

        <aside
          className={`right-context ${
            mobilePanel ? "mobile-open" : ""
          }`}
        >

          <div className="context-head">

            <span className="eyebrow">
              ACTIVE CONTEXT
            </span>

            <span className="context-indicator">
              LIVE
            </span>

          </div>

          <div className="context-block">
            <span className="context-key">MODE</span>
            <strong>adaptive-human</strong>
          </div>

          <div className="context-block">
            <span className="context-key">LANGUAGE</span>
            <strong>עברית · RTL</strong>
          </div>

          <div className="context-block">
            <span className="context-key">PRESENCE</span>
            <strong>נוכחת</strong>
          </div>

          <div className="context-avatar">
            <IMAAvatar />
          </div>

          <div className="context-note">

            <span className="quote-mark">
              “
            </span>

            <p>
              מחפשת אמת דרך חיבור בין חוויה אישית,
              יצירה ומערכות מורכבות.
            </p>

          </div>

        </aside>

      </div>

    </main>
  );
}
