import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { registerContinuity } from './services/deviceContinuity';
import { scheduleDeviceHealth } from './services/deviceHealth';

registerContinuity();
scheduleDeviceHealth();

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/Ima-kernel/sw.js', { scope: '/Ima-kernel/', updateViaCache: 'none' })
      .then(() => {
        if (navigator.serviceWorker.controller) {
          window.dispatchEvent(new Event('ima-service-worker-ready'));
        }
      })
      .catch(() => {});
  });
}

window.addEventListener('beforeinstallprompt', event => {
  event.preventDefault();
  window.__imaInstallPrompt = event;
  window.dispatchEvent(new Event('ima-install-available'));
});

window.addEventListener('appinstalled', () => {
  window.__imaInstallPrompt = null;
  window.__imaBeforeInstall = null;
  window.dispatchEvent(new Event('ima-install-completed'));
});

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
