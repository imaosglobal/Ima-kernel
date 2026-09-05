import { useState } from "react";
import { useI18n } from "./i18n/I18nProvider";
import { useUser } from "./hooks/useUser";
import Onboarding from "./components/Onboarding";
import Landing from "./components/Landing";
import ChatView from "./components/ChatView";
import MemoryView from "./components/MemoryView";
import SettingsView from "./components/SettingsView";
import StoreView from "./components/StoreView";
import IMAAvatar from "./components/IMAAvatar";
import LanguageSwitcher from "./components/LanguageSwitcher";
import "./App.css";

export default function App() {
  const { t } = useI18n();
  const {
    user,
    updateUser,
    completeOnboarding,
    addConversation,
    clearConversations,
    removeMemory,
    clearMemory,
    resetUser,
  } = useUser();

  const [view, setView] = useState("home");
  const [chatStarted, setChatStarted] = useState(false);
  const [initialMessage, setInitialMessage] = useState(null);

  // Onboarding
  if (!user.onboarded) {
    return <Onboarding onComplete={completeOnboarding} />;
  }

  function startChat(message) {
    setInitialMessage(message);
    setChatStarted(true);
    setView("home");
  }

  function goHome() {
    setView("home");
  }

  const navItems = [
    { id: "home", label: t("nav.home"), icon: "home" },
    { id: "store", label: t("nav.store"), icon: "store" },
    { id: "memory", label: t("nav.memory"), icon: "memory" },
    { id: "settings", label: t("nav.settings"), icon: "settings" },
  ];

  return (
    <div className="app-shell">
      {/* Header */}
      <header className="app-header">
        <button className="app-brand" onClick={goHome}>
          <IMAAvatar variant={user.avatar} size="xs" />
          <span className="app-brand-name">{t("brand.name")}</span>
        </button>
        <LanguageSwitcher />
      </header>

      {/* Main content */}
      <main className="app-main">
        {view === "home" && !chatStarted && (
          <Landing onStartChat={startChat} avatar={user.avatar} />
        )}
        {view === "home" && chatStarted && (
          <ChatView
            initialMessage={initialMessage}
            onClearInitial={() => setInitialMessage(null)}
            user={user}
          />
        )}
        {view === "store" && <StoreView />}
        {view === "memory" && (
          <MemoryView
            user={user}
            removeMemory={removeMemory}
            clearMemory={clearMemory}
            clearConversations={clearConversations}
          />
        )}
        {view === "settings" && (
          <SettingsView
            user={user}
            updateUser={updateUser}
            resetUser={() => {
              resetUser();
              setChatStarted(false);
              setView("home");
            }}
          />
        )}
      </main>

      {/* Bottom nav */}
      <nav className="app-nav">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`app-nav-btn ${view === item.id ? "app-nav-active" : ""}`}
            onClick={() => setView(item.id)}
          >
            <span className={`app-nav-icon app-nav-icon-${item.icon}`} />
            <span className="app-nav-label">{item.label}</span>
          </button>
        ))}
      </nav>
    </div>
  );
}
