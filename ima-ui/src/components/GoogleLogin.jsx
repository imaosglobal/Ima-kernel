import { useEffect, useRef, useState } from "react";
import "./GoogleLogin.css";

const GIS_URL = "https://accounts.google.com/gsi/client";
const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "";

function loadScript() {
  return new Promise((resolve) => {
    if (window.google?.accounts?.id) return resolve();
    const existing = document.querySelector(`script[src="${GIS_URL}"]`);
    if (existing) {
      existing.addEventListener("load", () => resolve());
      return;
    }
    const s = document.createElement("script");
    s.src = GIS_URL;
    s.async = true;
    s.defer = true;
    s.onload = () => resolve();
    document.head.appendChild(s);
  });
}

function decodeJWT(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
  } catch {
    return null;
  }
}

export default function GoogleLogin({ onSuccess, label = "Continue with Google" }) {
  const [ready, setReady] = useState(false);
  const btnRef = useRef(null);

  useEffect(() => {
    if (!CLIENT_ID) return;
    loadScript().then(() => {
      window.google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: (response) => {
          const data = decodeJWT(response.credential);
          if (data && onSuccess) {
            onSuccess({
              name: data.name || "",
              email: data.email || "",
              picture: data.picture || "",
              googleId: data.sub || "",
            });
          }
        },
      });
      setReady(true);
    });
  }, [onSuccess]);

  useEffect(() => {
    if (!ready || !btnRef.current) return;
    window.google.accounts.id.renderButton(btnRef.current, {
      type: "standard",
      shape: "pill",
      size: "large",
      text: "continue_with",
      locale: document.documentElement.lang || "en",
    });
  }, [ready]);

  if (!CLIENT_ID) {
    return (
      <button className="g-login-btn g-login-disabled" disabled>
        <span className="g-logo" />
        {label}
      </button>
    );
  }

  return <div className="g-login-wrapper" ref={btnRef} />;
}
