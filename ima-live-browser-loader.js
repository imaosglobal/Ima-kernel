(() => {
  const SERVICE = 'https://ima-browserglass.onrender.com/';
  const PANEL_ID = 'ima-live-browser-panel';
  const BUTTON_ID = 'ima-live-browser-launcher';

  function isLoggedIn() {
    const text = document.body?.innerText || '';
    return /התנתק|logout|sign out/i.test(text);
  }

  function create() {
    if (document.getElementById(PANEL_ID)) return;
    const panel = document.createElement('section');
    panel.id = PANEL_ID;
    panel.dir = 'rtl';
    panel.style.cssText = 'position:fixed;inset:auto 12px 12px 12px;z-index:2147483000;background:#08090d;border:1px solid rgba(255,255,255,.18);border-radius:16px;box-shadow:0 18px 60px rgba(0,0,0,.45);overflow:hidden;display:none;max-height:88vh;';
    panel.innerHTML = '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 10px;color:#fff;font:600 14px system-ui,sans-serif"><span>IMA — חלון עבודה חי</span><button type="button" data-close style="border:1px solid #555;background:#15171d;color:#fff;border-radius:8px;padding:6px 10px">סגור</button></div><iframe title="IMA Live Browser" src="' + SERVICE + '" style="display:block;width:100%;height:min(78vh,760px);border:0;background:#08090d" allow="clipboard-read; clipboard-write"></iframe>';
    panel.querySelector('[data-close]').onclick = () => { panel.style.display = 'none'; };
    document.body.appendChild(panel);
  }

  function open() {
    create();
    document.getElementById(PANEL_ID).style.display = 'block';
  }

  function wire() {
    create();
    const existing = [...document.querySelectorAll('button,a,[role="button"]')].find(el => /חלון עבודה חי|live browser/i.test(el.textContent || ''));
    if (existing) {
      if (!existing.dataset.imaBrowserGlassWired) {
        existing.dataset.imaBrowserGlassWired = '1';
        existing.addEventListener('click', e => {
          e.preventDefault();
          e.stopPropagation();
          if (!isLoggedIn()) {
            const target = document.querySelector('button');
            if (target) target.scrollIntoView({behavior:'smooth',block:'center'});
            return;
          }
          open();
        }, true);
      }
      return;
    }
    if (!document.getElementById(BUTTON_ID)) {
      const b = document.createElement('button');
      b.id = BUTTON_ID;
      b.type = 'button';
      b.textContent = 'פתח חלון עבודה חי';
      b.dir = 'rtl';
      b.style.cssText = 'position:fixed;right:12px;bottom:12px;z-index:2147482999;border:1px solid rgba(255,255,255,.25);background:#15171d;color:#fff;border-radius:10px;padding:10px 14px;font:600 14px system-ui,sans-serif';
      b.onclick = open;
      document.body.appendChild(b);
    }
  }

  const start = () => {
    wire();
    new MutationObserver(wire).observe(document.body, {childList:true,subtree:true});
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true});
  else start();
})();