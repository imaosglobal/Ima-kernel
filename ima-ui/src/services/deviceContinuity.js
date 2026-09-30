const KEY = 'ima-device-continuity-v1';

function classifyDevice() {
  const ua = navigator.userAgent || '';
  const platform = navigator.userAgentData?.platform || navigator.platform || '';
  const mobile = /Android|iPhone|iPad|iPod|Mobile/i.test(ua);
  const tablet = /iPad|Tablet/i.test(ua) || (/Android/i.test(ua) && !/Mobile/i.test(ua));
  const browser = /Chrome|Chromium|Firefox|Safari|Edge/i.test(ua) ? 'browser' : 'webview';
  let family = 'desktop-web';
  if (tablet) family = 'tablet-web';
  else if (mobile) family = /Android/i.test(ua) ? 'android-web' : 'ios-web';
  return { family, platform, browser, mobile, tablet, standalone: window.matchMedia?.('(display-mode: standalone)').matches === true };
}

export function getDeviceContinuity() {
  let installationId = localStorage.getItem(KEY);
  if (!installationId) {
    installationId = crypto.randomUUID();
    localStorage.setItem(KEY, installationId);
  }
  return {
    protocol: 'IMA-DEVICE-CONTINUITY-1.0',
    installationId,
    device: classifyDevice(),
    capabilities: {
      web: true,
      voiceInput: Boolean(window.SpeechRecognition || window.webkitSpeechRecognition),
      voiceOutput: Boolean(window.speechSynthesis),
      threeD: true,
      offlineShell: 'serviceWorker' in navigator,
      installable: true
    }
  };
}

export function registerContinuity() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/Ima-kernel/sw.js', { scope: '/Ima-kernel/' }).catch(() => {});
  }
  return getDeviceContinuity();
}