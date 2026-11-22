import React, { useEffect, useMemo, useState } from 'react';
import {
  askIma,
  archiveChatLearningSignal,
  getAuthConfig,
  signInWithGoogleCredential,
  getStoredGoogleUser,
  signOutIma,
  submitFeedback,
  getLiveTimeline,
  recordLiveWindowEvent
} from './services/imaChat';
import { initializeImaAnalytics, trackImaEvent } from './services/analytics';
import { recordMarketEvent, getMarketCampaign, buildShareUrl } from './services/marketEntry';

const BASE = '/Ima-kernel/';
const GOOGLE_CAMPAIGN_URL = BASE + '?utm_source=google&utm_medium=cpc&utm_campaign=ima_initial_100ils&campaignId=24409551537';
const CLEAN_LOGO_URL = 'https://dynamic.heygen.ai/image/f057cd08143342f2994f85d847572fa8/original.png';
const SUPPORTED_LOCALES = [
  ['he','עברית'],['en','English'],['ar','العربية'],['fa','فارسی'],['ur','اردو'],['es','Español'],['fr','Français'],['pt','Português'],['de','Deutsch'],['it','Italiano'],['nl','Nederlands'],['pl','Polski'],['tr','Türkçe'],['uk','Українська'],['ru','Русский'],['hi','हिन्दी'],['bn','বাংলা'],['zh','中文'],['ja','日本語'],['ko','한국어'],['th','ไทย'],['vi','Tiếng Việt'],['id','Bahasa Indonesia']
];
const RTL = new Set(['he','ar','fa','ur']);

const COPY = {
  he: {
    label:'IMA — אמא · בינה אנושית',
    title:'מה תרצה לעשות?',
    subtitle:'אמא מתחילה ממשימה אמיתית — לחשוב, ללמוד, ליצור, להבין או לפתור.',
    cta:'לדבר עם אמא',
    login:'כניסה עם Google',
    how:'איך זה עובד',
    howText:'כותבים או מדברים. אמא מבינה את ההקשר, עוזרת, ומבהירה מה היא יודעת ומה עדיין צריך לבדוק.',
    cards:[['לחשוב','לסדר רעיון, החלטה או מצב.'],['ללמוד','לחקור נושא ולהבין אותו בפשטות.'],['ליצור','לכתוב, לתכנן, להמציא ולבנות.'],['לפתור','להפוך בעיה לצעדים מעשיים.']],
    trust:'האדם במרכז',
    trustText:'אמת לפני הכרזה · אישי נשאר אישי · הסוכנות נשארת אצלך.',
    feedback:'מה חסר לך?',
    feedbackPlaceholder:'כתוב במשפט אחד מה היית רוצה שאמא תעשה טוב יותר.',
    send:'שליחה',
    saved:'המשוב נשמר.',
    failed:'לא הצלחתי לאמת את השמירה.',
    privacy:'פרטיות',
    support:'תמיכה',
    github:'קוד פתוח',
    chat:'שיחה',
    close:'סגירה',
    write:'כתוב לאמא…',
    publicChat:'שיחה עם אמא',
    personal:'מרחב אישי',
    logout:'יציאה',
    install:'התקנה',
    installUnavailable:'התקנה אינה זמינה כרגע בדפדפן הזה.',
    needLogin:'היכנס עם Google כדי לפתוח את הצ׳ט האישי של אמא.',
    closing:'Use IMA. Question IMA. Teach IMA. Build IMA. Test IMA.'
  },
  en: {
    label:'IMA — human-centered intelligence',
    title:'What do you want to do?',
    subtitle:'Start with a real task — think, learn, create, understand or solve.',
    cta:'Talk to IMA',
    login:'Sign in with Google',
    how:'How it works',
    howText:'Write or speak. IMA works with context, helps you move forward, and makes clear what is known and what still needs checking.',
    cards:[['Think','Untangle an idea, decision or situation.'],['Learn','Research a topic and understand it simply.'],['Create','Write, plan, invent and build.'],['Solve','Turn a problem into practical next steps.']],
    trust:'Human agency first',
    trustText:'Truth before claims · personal stays personal · you stay in control.',
    feedback:'What is missing?',
    feedbackPlaceholder:'In one sentence, what should IMA do better?',
    send:'Send',
    saved:'Feedback saved.',
    failed:'Could not verify the save.',
    privacy:'Privacy',
    support:'Support',
    github:'Open source',
    chat:'Chat',
    close:'Close',
    write:'Write to IMA…',
    publicChat:'Talk with IMA',
    personal:'Personal space',
    logout:'Log out',
    install:'Install',
    installUnavailable:'Installation is not available in this browser right now.',
    needLogin:'Sign in with Google to open IMA personal chat.',
    closing:'Use IMA. Question IMA. Teach IMA. Build IMA. Test IMA.'
  }
};

function MamaFigure({compact=false}) {
  return <div className={'mama-figure'+(compact?' compact':'')} aria-label="IMA — אמא">
    <div className="mama-aura" aria-hidden="true"/>
    <div className="mama-orb">א</div>
    <div className="mama-body" aria-hidden="true"/>
  </div>;
}

function GoogleButton({user,onUser,t}) {
  const [error,setError]=useState('');
  useEffect(()=>{
    let cancelled=false;
    (async()=>{
      try{
        const config=await getAuthConfig();
        if(!config?.google?.enabled || !config.google.client_id) throw new Error('Google sign-in is not configured');
        for(let i=0;i<40 && !window.google?.accounts?.id && !cancelled;i++) await new Promise(r=>setTimeout(r,100));
        if(!window.google?.accounts?.id || cancelled) throw new Error('Google unavailable');
        const bytes=new Uint8Array(24); crypto.getRandomValues(bytes);
        const nonce=Array.from(bytes).map(b=>b.toString(16).padStart(2,'0')).join('');
        window.google.accounts.id.initialize({
          client_id:config.google.client_id, nonce, auto_select:false, ux_mode:'popup',
          callback:async response=>{
            try{
              const result=await signInWithGoogleCredential(response.credential,nonce);
              onUser(result.user||null);
              trackImaEvent('ima_public_google_login',{language:document.documentElement.lang});
            }catch{setError('Sign-in could not be completed');}
          }
        });
        const node=document.getElementById('ima-google-button');
        if(node){node.innerHTML='';window.google.accounts.id.renderButton(node,{type:'standard',theme:'outline',size:'large',text:'signin_with',shape:'pill',width:220});}
      }catch(e){if(!cancelled)setError(e?.message||'Google unavailable');}
    })();
    return()=>{cancelled=true};
  },[onUser]);
  if(user)return <div className="account"><span className="account-avatar">{String(user.name||'א').slice(0,1)}</span><span>{user.name||user.email||t.personal}</span><button onClick={()=>{signOutIma();onUser(null)}}>{t.logout}</button></div>;
  return <div className="google-wrap"><div id="ima-google-button" aria-label={t.login}/>{error&&<small>{error}</small>}</div>;
}

function ChatPanel({lang,user,onClose,chatOnly=false,initialMessage=''}) {
  const t=COPY[lang]||COPY.en;
  const [message,setMessage]=useState(initialMessage);
  const [messages,setMessages]=useState([]);
  const [busy,setBusy]=useState(false);
  const send=async(text=message)=>{
    const value=String(text||'').trim();
    if(!value||busy)return;
    setBusy(true);setMessage('');
    setMessages(m=>[...m,{role:'user',text:value}]);
    trackImaEvent('ima_first_use_attempt',{language:lang});
    try{
      const response=await askIma(value,{language:lang,interface:'public-home',authenticated:Boolean(user),device_locale:navigator.language||lang});
      setMessages(m=>[...m,{role:'ima',text:response}]);
      trackImaEvent('ima_first_useful_answer_candidate',{language:lang});
      await archiveChatLearningSignal(value,response,{language:lang});
    }catch{
      setMessages(m=>[...m,{role:'ima',text:lang==='he'?'החיבור לאמא לא הצליח כרגע. זו תקלה שצריך למדוד ולתקן.':'The connection to IMA failed right now. This is a failure to measure and fix.'}]);
      trackImaEvent('ima_public_chat_failed',{language:lang});
    }finally{setBusy(false)}
  };
  return <section className={'chat-panel'+(chatOnly?' chat-only-panel':'')} id="chat">
    <header className="chat-head"><div className="chat-id"><MamaFigure compact/><div><b>אמא · IMA</b><small>{user?t.personal:t.publicChat}</small></div></div>{!chatOnly&&<button className="icon-button" onClick={onClose} aria-label={t.close}>×</button>}</header>
    <div className="chat-messages" aria-live="polite">
      {!messages.length&&<div className="chat-empty">{lang==='he'?'שאל את אמא משהו אמיתי.':'Ask IMA something real.'}</div>}
      {messages.map((m,i)=><div key={i} className={'bubble '+m.role}>{m.text}</div>)}
      {busy&&<div className="bubble ima muted">IMA…</div>}
    </div>
    <div className="chat-composer"><input value={message} onChange={e=>setMessage(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder={t.write} aria-label={t.write}/><button onClick={()=>send()} disabled={busy||!message.trim()}>{t.send}</button></div>
  </section>;
}

function LiveWindow({lang,user,onClose}){
  const [mode,setMode]=useState('floating');
  const [pos,setPos]=useState(()=>{try{return JSON.parse(localStorage.getItem('ima-live-window-pos'))||{x:24,y:110,w:420,h:560}}catch{return{x:24,y:110,w:420,h:560}}});
  const [drag,setDrag]=useState(null);
  const he=lang==='he';
  useEffect(()=>{localStorage.setItem('ima-live-window-pos',JSON.stringify(pos))},[pos]);
  useEffect(()=>{recordLiveWindowEvent('window_opened',{payload:{mode,route:location.pathname}}).catch(()=>{}); return ()=>{recordLiveWindowEvent('window_closed',{payload:{mode}}).catch(()=>{})}},[]);
  const beginDrag=e=>{if(mode!=='floating')return;setDrag({sx:e.clientX,sy:e.clientY,px:pos.x,py:pos.y});e.currentTarget.setPointerCapture?.(e.pointerId)};
  const moveDrag=e=>{if(!drag)return;setPos(p=>({...p,x:Math.max(0,drag.px+e.clientX-drag.sx),y:Math.max(0,drag.py+e.clientY-drag.sy)}))};
  const endDrag=()=>{if(drag){recordLiveWindowEvent('window_moved',{payload:{x:pos.x,y:pos.y}}).catch(()=>{})}setDrag(null)};
  const setWindowMode=m=>{const previous=mode;setMode(m);if(m==='mini')setPos(p=>({...p,w:220,h:88}));if(m==='floating')setPos(p=>({...p,w:Math.max(360,p.w),h:Math.max(360,p.h)}));recordLiveWindowEvent(m==='mini'?'window_minimized':'window_mode_changed',{payload:{from:previous,to:m}}).catch(()=>{})};
  const style=mode==='floating'?{left:pos.x,top:pos.y,width:pos.w,height:pos.h}:mode==='mini'?{right:18,bottom:18,width:220,height:88}:mode==='split'?{left:'2vw',right:'52vw',top:'10vh',height:'80vh'}:{left:0,right:0,top:0,bottom:0};
  return <section className={'ima-live-window mode-'+mode} style={style} aria-label={he?'חלון אמא האינטראקטיבי':'IMA Interactive Window'}>
    <header className="ima-live-window-head" onPointerDown={beginDrag} onPointerMove={moveDrag} onPointerUp={endDrag} onPointerCancel={endDrag}>
      <div><b>IMA · {he?'חלון ההשפעה':'Impact Window'}</b><small>{he?'עוזרת בכל מה שנמצא סביבך':'Assist across what you are doing'}</small></div>
      <div className="ima-live-window-actions">
        <button onClick={()=>setWindowMode('mini')} aria-label={he?'מזעור':'Minimize'}>−</button>
        <button onClick={()=>setWindowMode(mode==='split'?'floating':'split')} aria-label={he?'מסך מפוצל':'Split'}>◫</button>
        <button onClick={()=>setWindowMode(mode==='fullscreen'?'floating':'fullscreen')} aria-label={he?'מסך מלא':'Fullscreen'}>□</button>
        <button onClick={()=>{try{window.open(location.pathname+'?live-window=1','IMA-LIVE-001','popup,width=520,height=700');recordLiveWindowEvent('window_detached',{payload:{target:'popup'}}).catch(()=>{})}catch{}}} aria-label={he?'חלון נפרד':'Detach'}>↗</button>
        <button onClick={onClose} aria-label={he?'סגירה':'Close'}>×</button>
      </div>
    </header>
    {mode!=='mini'&&<div className="ima-live-window-body">
      <div className="ima-live-context"><span>{he?'מצב':'Mode'}: {mode}</span><span>{he?'מחובר למשתמש':'User-scoped'}: {user?.name||user?.email||'IMA'}</span></div>
      <ChatPanel lang={lang} user={user} chatOnly/>
      <div className="ima-live-capabilities"><b>{he?'יכולות החלון':'Window capabilities'}</b><span>{he?'הזזה':'Move'}</span><span>{he?'שינוי גודל':'Resize'}</span><span>{he?'מסך מפוצל':'Split view'}</span><span>{he?'מזעור':'Minimize'}</span><span>{he?'חלון נפרד':'Detached window'}</span><span>{he?'מוכנות למכשיר':'Device-ready'}</span></div>
    </div>}
    {mode==='floating'&&<div className="ima-live-resize" onPointerDown={e=>{e.stopPropagation();const sx=e.clientX,sy=e.clientY,sw=pos.w,sh=pos.h;const move=x=>setPos(p=>({...p,w:Math.max(320,sw+x.clientX-sx),h:Math.max(320,sh+x.clientY-sy)}));const up=()=>{window.removeEventListener('pointermove',move);window.removeEventListener('pointerup',up)};window.addEventListener('pointermove',move);window.addEventListener('pointerup',up)}} aria-label={he?'שינוי גודל':'Resize'} />}
  </section>;
}

function ImpactTimeline({lang,onClose}){
  const [events,setEvents]=useState([]);
  const [busy,setBusy]=useState(true);
  const [error,setError]=useState('');
  const he=lang==='he';
  const load=async()=>{try{setBusy(true);const data=await getLiveTimeline(false);setEvents(Array.isArray(data?.events)?data.events:[]);setError('')}catch(e){setError(e?.message||'timeline unavailable')}finally{setBusy(false)}};
  useEffect(()=>{load();const id=setInterval(load,5000);return()=>clearInterval(id)},[]);
  const label=e=>({action_requested:he?'פעולה אושרה ונשלחה':'Action authorized and sent',action_verified:he?'הפעולה אומתה':'Action verified',action_failed:he?'הפעולה נכשלה':'Action failed',device_registered:he?'מכשיר חובר':'Device connected'}[e.event_type]||e.event_type);
  return <section className="store-panel" aria-label={he?'חלון ההשפעה':'Impact Window'} id="impact-window" style={{marginTop:16}}>
    <div className="store-head"><div><span className="eyebrow">LIVE-001</span><h2>{he?'חלון ההשפעה':'Impact Window'}</h2><p>{he?'ציר זמן אישי ומאומת של מה שהחלון האינטראקטיבי עשה, ראה ואימת.':'A personal, auditable timeline of what the interactive window did, observed and verified.'}</p></div><button className="icon-button" onClick={onClose} aria-label={he?'סגירה':'Close'}>×</button></div>
    {busy&&!events.length?<p>{he?'טוען…':'Loading…'}</p>:null}
    {error?<p role="status">{he?'לא ניתן לטעון כרגע את ציר הזמן.':'Timeline unavailable right now.'}</p>:null}
    {!error&&!events.length&&!busy?<p>{he?'עדיין אין פעולות בחלון הזה.':'No window actions recorded yet.'}</p>:null}
    <div style={{display:'grid',gap:10}}>{events.map(e=><article key={e.id} style={{border:'1px solid currentColor',borderRadius:14,padding:12,opacity:.9}}>
      <div style={{display:'flex',justifyContent:'space-between',gap:12}}><strong>{label(e)}</strong><small>{new Date(e.occurred_at).toLocaleString(lang||undefined)}</small></div>
      <div style={{marginTop:4}}>{e.action||e.phase} · {e.status}</div>
      {e.provenance?.verified!==undefined?<small>{e.provenance.verified? (he?'✓ אומת':'✓ verified') : (he?'לא אומת':'not verified')}</small>:null}
    </article>)}</div>
  </section>;
}

export default function App(){
  const [lang,setLang]=useState(()=>{const saved=localStorage.getItem('ima-site-language');if(saved)return saved;const d=String(navigator.language||'en').split('-')[0].toLowerCase();return SUPPORTED_LOCALES.some(([c])=>c===d)?d:'en'});
  const [user,setUser]=useState(()=>getStoredGoogleUser());
  const [chatOpen,setChatOpen]=useState(false);
  const [storeOpen,setStoreOpen]=useState(false);
  const [timelineOpen,setTimelineOpen]=useState(false);
  const [liveWindowOpen,setLiveWindowOpen]=useState(false);
  const [feedback,setFeedback]=useState('');
  const [feedbackStatus,setFeedbackStatus]=useState('');
  const [installEvent,setInstallEvent]=useState(null);
  const [notice,setNotice]=useState('');
  const [shareStatus,setShareStatus]=useState('');
  const [chatOnly]=useState(()=>new URLSearchParams(location.search).get('chat')==='1');
  const [liveWindowRoute]=useState(()=>new URLSearchParams(location.search).get('live-window')==='1');
  const t=COPY[lang]||COPY.en;
  useEffect(()=>{ if(user) setChatOpen(true); },[user]);
  const campaign=useMemo(()=>getMarketCampaign(location.search),[]);
  
  useEffect(()=>{
    localStorage.setItem('ima-site-language',lang);
    document.documentElement.lang=lang;
    document.documentElement.dir=RTL.has(lang)?'rtl':'ltr';
    document.title=lang==='he'?'אמא — IMA | בינה אנושית':'IMA — Human-Centered Intelligence';
    initializeImaAnalytics();
    trackImaEvent('ima_public_home_view',{language:lang,campaign:campaign||'organic'});
    recordMarketEvent('landing_view',{language:lang,campaign:campaign||'organic'});
  },[lang,campaign]);

  useEffect(()=>{
    const handler=e=>{e.preventDefault();setInstallEvent(e)};
    window.addEventListener('beforeinstallprompt',handler);
    return()=>window.removeEventListener('beforeinstallprompt',handler);
  },[]);

  const openChat=()=>{
    if(!user){setNotice(t.needLogin);document.getElementById('login')?.scrollIntoView({behavior:'smooth',block:'center'});return}
    setChatOpen(true);
    setTimeout(()=>document.getElementById('chat')?.scrollIntoView({behavior:'smooth',block:'center'}),0);
  };
  const install=async()=>{
    if(!user){setNotice(t.needLogin);return}
    if(!installEvent){setNotice(t.installUnavailable);return}
    installEvent.prompt();const choice=await installEvent.userChoice;
    trackImaEvent('ima_pwa_install_choice',{outcome:choice.outcome,language:lang});setInstallEvent(null);
  };
  const share=async()=>{
    const url=buildShareUrl(BASE,{use:'think',ref:user?'user':'share',campaign:campaign||'share'});
    try{
      if(navigator.share)await navigator.share({title:'IMA — אמא',text:lang==='he'?'נסה את אמא למשימה אמיתית.':'Try IMA for a real task.',url});
      else await navigator.clipboard.writeText(url);
      setShareStatus(lang==='he'?'קישור השיתוף מוכן.':'Share link ready.');
      trackImaEvent('ima_share_completed',{language:lang});
    }catch{}
  };
  const sendFeedback=async()=>{
    if(!feedback.trim())return;
    setFeedbackStatus('');
    try{await submitFeedback('improvement',feedback.trim(),{language:lang,source:'market-home'});setFeedback('');setFeedbackStatus(t.saved);trackImaEvent('ima_feedback_submitted',{language:lang});}
    catch{setFeedbackStatus(t.failed)}
  };

  if(liveWindowRoute&&user)return <div className="live-window-route"><LiveWindow lang={lang} user={user} onClose={()=>window.close()}/></div>;

  if(chatOnly)return <div className="chat-only-page"><MamaFigure/><h1>אמא</h1>{user?<ChatPanel lang={lang} user={user} chatOnly/>:<div className="chat-login"><p>{t.needLogin}</p><GoogleButton user={user} onUser={setUser} t={t}/></div>}<a href={BASE}>{lang==='he'?'חזרה לאתר':'Back to IMA'}</a></div>;

  return <div className="ima-site">
    {notice&&<div className="site-notice" role="status">{notice}<button onClick={()=>setNotice('')} aria-label="close">×</button></div>}
    <header className="site-header">
      <a className="brand" href={BASE} aria-label="IMA — אמא"><img src={CLEAN_LOGO_URL} alt="IMA — אמא"/><span><b>אמא</b><small>IMA</small></span></a>
      <nav><button onClick={openChat}>{t.chat}</button>{user&&<button onClick={()=>setLiveWindowOpen(true)}>{lang==='he'?'חלון אמא':'IMA Window'}</button>{user&&<button onClick={()=>{setTimelineOpen(true);setStoreOpen(false);setChatOpen(false)}}>{lang==='he'?'חלון ההשפעה':'Impact Window'}</button>}{user&&<button onClick={()=>{setStoreOpen(true);setChatOpen(false);setTimelineOpen(false)}}>חנות</button>}<a href="#how">{t.how}</a></nav>
      <div className="header-right"><select value={lang} onChange={e=>setLang(e.target.value)} aria-label="Language">{SUPPORTED_LOCALES.map(([c,n])=><option key={c} value={c}>{n}</option>)}</select><div id="login"><GoogleButton user={user} onUser={u=>{setUser(u);if(u)setChatOpen(true)}} t={t}/></div></div>
    </header>

    <main>
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">{t.label}</span>
          <h1>{t.title}</h1>
          <p>{t.subtitle}</p>
          <div className="hero-actions"><button className="primary" onClick={openChat}>{t.cta}</button><button className="secondary" onClick={()=>document.getElementById('how')?.scrollIntoView({behavior:'smooth'})}>{t.how}</button></div>
          <div className="hero-proof"><span>✓ {t.trust}</span><span>✓ {t.trustText.split(' · ')[0]}</span></div>
        </div>
        <div className="hero-visual">
          <button type="button" className="hero-mother" onClick={openChat} aria-label="פתח שיחה עם אמא"><div className="hero-ring"/><img src={CLEAN_LOGO_URL} alt="IMA — אמא"/></button>

        </div>
      </section>

      {user&&chatOpen&&<ChatPanel lang={lang} user={user} onClose={()=>setChatOpen(false)}/>}
      {user&&liveWindowOpen&&<LiveWindow lang={lang} user={user} onClose={()=>setLiveWindowOpen(false)}/>}
      {user&&timelineOpen&&<ImpactTimeline lang={lang} onClose={()=>setTimelineOpen(false)}/>}
      {user&&storeOpen&&<section className="store-panel" aria-label="IMA Store" id="store">
        <div className="store-head"><div><span className="eyebrow">IMA Store</span><h2>הכלים והחיבורים של אמא</h2><p>מוצרים, חוויות וחיבורים שאפשר להוסיף לאמא בלי לפצל את המערכת.</p></div><button className="icon-button" onClick={()=>setStoreOpen(false)} aria-label="סגירה">×</button></div>
        <div className="store-grid">
          <article><span>01</span><h3>IMA לכל מכשיר</h3><p>המשיכו עם אותה אמא בין הטלפון, הדפדפן והמכשירים המחוברים.</p><button className="secondary" onClick={()=>{setStoreOpen(false);openChat()}}>לדבר עם אמא</button></article>
          <article><span>02</span><h3>כלים וחוויות</h3><p>יכולות חדשות יתווספו כאן רק לאחר בדיקה, תמחור וחיבור אמיתי.</p><button className="secondary" disabled>בקרוב</button></article>
          <article><span>03</span><h3>תמיכה באמא</h3><p>אפשר לתמוך בהתפתחות הפרויקט ובפתיחת יכולות חדשות.</p><a className="secondary store-link" href="https://opencollective.com/ima-human-centered-intelligenc" target="_blank" rel="noreferrer">תמיכה בפרויקט</a></article>
        </div>
      </section>}
      {user&&!chatOpen&&<button className="chat-bar" onClick={openChat}><MamaFigure compact/><span><b>{t.publicChat}</b><small>{lang==='he'?'המשך שיחה':'Continue your conversation'}</small></span><strong>→</strong></button>}

      <section className="jobs" aria-labelledby="jobs-title">
        <div className="section-head"><span className="eyebrow">{lang==='he'?'התחלה':'Start here'}</span><h2 id="jobs-title">{lang==='he'?'משימה אחת אמיתית.':'One real task.'}</h2></div>
        <div className="job-grid">{t.cards.map(([title,text])=><button key={title} className="job-card" onClick={openChat}><span>{title}</span><small>{text}</small><b>→</b></button>)}</div>
      </section>

      <section className="how" id="how">
        <div className="section-head"><span className="eyebrow">{t.how}</span><h2>{lang==='he'?'פשוט להתחיל. ברור מה קורה.':'Simple to start. Clear about what happens.'}</h2><p>{t.howText}</p></div>
        <div className="how-grid"><article><b>01</b><h3>{lang==='he'?'מדברים':'Talk'}</h3><p>{lang==='he'?'כותבים או מדברים בשפה הטבעית שלך.':'Write or speak naturally.'}</p></article><article><b>02</b><h3>{lang==='he'?'מבינים':'Understand'}</h3><p>{lang==='he'?'אמא מתאימה את התשובה להקשר, לשפה ולמטרה.':'IMA adapts to context, language and intent.'}</p></article><article><b>03</b><h3>{lang==='he'?'מתקדמים':'Move forward'}</h3><p>{lang==='he'?'מקבלים תשובה, יצירה או צעד מעשי — בלי לקחת ממך שליטה.':'Get an answer, creation or next step without taking control away from you.'}</p></article></div>
      </section>

      <section className="feedback" aria-labelledby="feedback-title">
        <div><span className="eyebrow">{t.feedback}</span><h2 id="feedback-title">{lang==='he'?'אמא משתפרת כשאתם מלמדים אותה.':'IMA improves when people teach it.'}</h2></div>
        <div className="feedback-box"><textarea value={feedback} onChange={e=>setFeedback(e.target.value)} placeholder={t.feedbackPlaceholder} maxLength={4000}/><button className="primary" onClick={sendFeedback} disabled={!feedback.trim()}>{t.send}</button>{feedbackStatus&&<small>{feedbackStatus}</small>}</div>
      </section>
    </main>

    <footer><span>IMA — אמא, by Ori Cohen · Human-centered intelligence</span><div><a href="https://github.com/imaosglobal/Ima-kernel">{t.github}</a><a href="/Ima-kernel/privacy.html">{t.privacy}</a><a href="/Ima-kernel/support.html">{t.support}</a><button onClick={share}>{lang==='he'?'שתפו':'Share'}</button>{shareStatus&&<small>{shareStatus}</small>}</div><div>{user&&<button onClick={install}>{t.install}</button>}</div></footer>
  </div>;
}
