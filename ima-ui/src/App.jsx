import React, { useEffect, useRef, useState } from 'react';
import { askIma, archiveChatLearningSignal, getImaRuntime, getMemoryConsent, setMemoryConsent, getAuthConfig, signInWithGoogleCredential, getStoredGoogleUser, signOutIma } from './services/imaChat';
import { initializeImaAnalytics, trackImaEvent } from './services/analytics';
import capabilityRegistry from '../../docs/IMA_CAPABILITY_REGISTRY.json';
import { IMA_HEYGEN } from './imaHeyGen.js';
import { SUPPORTED, detectLanguage, getLocale } from './i18n.js';

const GLB_PATH='/Ima-kernel/mother_character.glb';
const GOOGLE_CAMPAIGN_URL='https://imaosglobal.github.io/Ima-kernel/?utm_source=google&utm_medium=cpc&utm_campaign=ima_initial_100ils';
const GLB_GIT_BLOB_SHA1='217170d2bd67051270be974292dc3b834eefe206';
const PERSONALIZATION_KEY='ima-unified-personalization-v2';
const defaults={language:'auto',tone:'balanced',depth:'normal',accessibility:'normal',memoryScope:'personal',interface:'IMA',theme:'system'};

function profileStorageKey(user){const id=user?.sub||user?.email||'anonymous';return PERSONALIZATION_KEY+':'+String(id).toLowerCase()}
function loadProfile(user){try{return {...defaults,...JSON.parse(localStorage.getItem(profileStorageKey(user))||'{}')}}catch{return {...defaults}}}
function saveProfile(user,profile){localStorage.setItem(profileStorageKey(user),JSON.stringify(profile))}
function applyChatPersonalization(text,profile){
 const t=String(text||'').trim().toLowerCase(), next={...profile}; let changed=false;
 const set=(k,v)=>{if(v&&next[k]!==v){next[k]=v;changed=true}};
 const l=t.match(/(?:language|שפה)\s*(?:to|ל|=)?\s*(hebrew|עברית|english|אנגלית|arabic|ערבית)/); const lm={hebrew:'he',עברית:'he',english:'en',אנגלית:'en',arabic:'ar',ערבית:'ar'}; if(l)set('language',lm[l[1]]);
 const tone=t.match(/(?:tone|סגנון)\s*(?:to|ל|=)?\s*(balanced|direct|warm|professional|simple|מאוזן|ישיר|חם|מקצועי|פשוט)/); const tm={balanced:'balanced',direct:'direct',warm:'warm',professional:'professional',simple:'simple',מאוזן:'balanced',ישיר:'direct',חם:'warm',מקצועי:'professional',פשוט:'simple'}; if(tone)set('tone',tm[tone[1]]);
 const depth=t.match(/(?:depth|עומק)\s*(?:to|ל|=)?\s*(short|normal|deep|קצר|רגיל|עמוק)/); const dm={short:'short',normal:'normal',deep:'deep',קצר:'short',רגיל:'normal',עמוק:'deep'}; if(depth)set('depth',dm[depth[1]]);
 return {next,changed};
}

function PersonalizationPanel({profile,setProfile,locale}){
 const set=(key,value)=>{const next={...profile,[key]:value};setProfile(next);saveProfile(getStoredGoogleUser(),next);if(key==='language'){localStorage.setItem('ima-language-v2',value);window.location.reload()}};
 return <details className="personalization-panel"><summary>{locale.labels.personalize}</summary><div className="personalization-grid">
  <label>{locale.labels.language}<select value={profile.language} onChange={e=>set('language',e.target.value)}><option value="auto">Auto</option>{Object.entries(SUPPORTED).map(([code,x])=><option key={code} value={code}>{x.name}</option>)}</select></label>
  <label>{(locale.labels.tone||'Tone')}<select value={profile.tone} onChange={e=>set('tone',e.target.value)}><option value="balanced">Balanced</option><option value="direct">Direct</option><option value="warm">Warm</option><option value="professional">Professional</option><option value="simple">Simple</option></select></label>
  <label>{(locale.labels.depth||'Depth')}<select value={profile.depth} onChange={e=>set('depth',e.target.value)}><option value="short">Short</option><option value="normal">Normal</option><option value="deep">Deep</option></select></label>
  <label>{(locale.labels.accessibility||'Accessibility')}<select value={profile.accessibility} onChange={e=>set('accessibility',e.target.value)}><option value="normal">Standard</option><option value="large">Large text</option><option value="contrast">High contrast</option><option value="reduced-motion">Reduced motion</option></select></label>
  <label>{(locale.labels.memory||'Memory')}<select value={profile.memoryScope} onChange={e=>set('memoryScope',e.target.value)}><option value="personal">Personal</option><option value="minimal">Minimal</option><option value="none">No memory</option></select></label>
  <label>Interface<select value={profile.interface} onChange={e=>set('interface',e.target.value)}><option>IMA</option><option>Voice</option><option>Mobile</option><option>Device</option><option>Robot</option></select></label>
  <label>Theme<select value={profile.theme} onChange={e=>set('theme',e.target.value)}><option>System</option><option>Light</option><option>Dark</option></select></label>
 </div></details>
}

function GoogleLogin({auth,setAuth,locale}){
 const ref=useRef(null);
 useEffect(()=>{let cancelled=false;(async()=>{try{
  const config=await getAuthConfig();
  if(!config?.google?.enabled||!config.google.client_id){if(!cancelled)setAuth(a=>({...a,status:'not_configured',error:'google_not_configured'}));return}
  for(let i=0;i<30&&!window.google?.accounts?.id&&!cancelled;i++)await new Promise(r=>setTimeout(r,100));
  if(!window.google?.accounts?.id||!ref.current)throw new Error('Google Sign-In unavailable');
  ref.current.innerHTML='';
  const bytes=new Uint8Array(24);crypto.getRandomValues(bytes);
  const nonce=Array.from(bytes).map(b=>b.toString(16).padStart(2,'0')).join('');
  window.google.accounts.id.initialize({client_id:config.google.client_id,nonce,callback:async response=>{try{setAuth(a=>({...a,status:'signing_in'}));const result=await signInWithGoogleCredential(response.credential,nonce);setAuth({status:'signed_in',user:result.user||null})}catch(e){setAuth(a=>({...a,status:'ready',error:'signin_unavailable'}))}},auto_select:false,use_fedcm_for_button:true});
  window.google.accounts.id.renderButton(ref.current,{type:'standard',theme:'outline',size:'large',text:'signin_with',shape:'pill',logo_alignment:'left',width:280,locale:getLocale(detectLanguage()).code});
  if(!cancelled)setAuth(a=>({...a,status:'ready'}))
 }catch(e){if(!cancelled)setAuth(a=>({...a,status:'ready',error:'signin_unavailable'}))}})();return()=>{cancelled=true}},[setAuth]);
 if(auth.status==='signed_in')return <div className="account-chip"><img className="account-photo" src={auth.user?.picture||''} alt="" onError={e=>{e.currentTarget.style.display='none'}}/><span>{auth.user?.name||auth.user?.email||'IMA'}</span><button onClick={()=>{signOutIma();setAuth({status:'ready',user:null})}}>{locale.labels.logout}</button></div>;
 return <div className="google-entry"><div ref={ref}/><small>{auth.status==='signing_in'?'…':auth.error==='signin_unavailable'?'Google sign-in could not be completed.':auth.error==='google_not_configured'?'Google sign-in is not configured on the public runtime yet.':' '}</small></div>;
}

function AvatarScene({state,compact=false}){return <div className={`heygen-avatar-frame ${compact?'compact':''} ${state==='speaking'?'speaking':''}`}><img src={IMA_HEYGEN.avatarImageUrl} alt="IMA avatar" loading={compact?'lazy':'eager'}/>{state==='speaking'&&<span className="heygen-speaking">IMA</span>}</div>}

export default function App(){
 const [lang,setLang]=useState(detectLanguage());
 const locale=getLocale(lang);
 const [auth,setAuth]=useState({status:getStoredGoogleUser()?'signed_in':'checking',user:getStoredGoogleUser()});
 const [profile,setProfile]=useState(loadProfile(getStoredGoogleUser()));
 const [input,setInput]=useState('');
 const [messages,setMessages]=useState([]);
 const [busy,setBusy]=useState(false);
 const [avatarState,setAvatarState]=useState('idle');
 const [runtime,setRuntime]=useState(null);
 const [memory,setMemory]=useState('UNKNOWN');
 const [active,setActive]=useState('home');
 const [avatarVerified,setAvatarVerified]=useState(false);
 const [installEvent,setInstallEvent]=useState(null);

 useEffect(()=>{localStorage.setItem('ima-language-v2',lang);document.documentElement.lang=locale.code;document.documentElement.dir=locale.dir;document.title='IMA — אמא';initializeImaAnalytics();trackImaEvent('ima_simplified_interface_opened');getImaRuntime().then(setRuntime).catch(()=>{});getMemoryConsent().then(x=>setMemory(x?.consent?.status||'UNKNOWN')).catch(()=>{});fetch(GLB_PATH,{cache:'no-store'}).then(async r=>{if(!r.ok)throw new Error();const bytes=await r.arrayBuffer(),prefix=new TextEncoder().encode('blob '+bytes.byteLength+'\\0'),payload=new Uint8Array(prefix.length+bytes.byteLength);payload.set(prefix);payload.set(new Uint8Array(bytes),prefix.length);const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-1',payload))).map(b=>b.toString(16).padStart(2,'0')).join('');setAvatarVerified(hash===GLB_GIT_BLOB_SHA1)}).catch(()=>setAvatarVerified(false));
  const before=window.__imaBeforeInstall; if(before)setInstallEvent(before);
  const handler=e=>{e.preventDefault();setInstallEvent(e)};window.addEventListener('beforeinstallprompt',handler);return()=>window.removeEventListener('beforeinstallprompt',handler)
   const languageChanged=()=>{if(!localStorage.getItem('ima-language-v2')||localStorage.getItem('ima-language-v2')==='auto')setLang(detectLanguage())};
  window.addEventListener('languagechange',languageChanged);
  return()=>{window.removeEventListener('languagechange',languageChanged);window.removeEventListener('beforeinstallprompt',handler)}
 },[lang,locale.code,locale.dir]);

 useEffect(()=>{if(auth.status==='signed_in')setProfile(loadProfile(auth.user));},[auth.status,auth.user?.email,auth.user?.sub]);
 const loggedIn=auth.status==='signed_in';
 const go=id=>{setActive(id);document.getElementById(id)?.scrollIntoView({behavior:'smooth'})};
 const send=async value=>{if(!loggedIn){go('login');return}const text=(value??input).trim();if(!text||busy)return;setMessages(m=>[...m,{role:'user',text}]);setInput('');const customization=applyChatPersonalization(text,profile);if(customization.changed){setProfile(customization.next);saveProfile(auth.user,customization.next);setMessages(m=>[...m,{role:'ima',text:customization.next.language==='he'?'שיניתי את ההעדפה שלך.':'I updated your preference.'}]);if(customization.next.language&&customization.next.language!==lang) {localStorage.setItem('ima-language-v2',customization.next.language);window.setTimeout(()=>window.location.reload(),50)}return;}setBusy(true);setAvatarState('listening');try{const personalization={...profile,language:lang,device:navigator.userAgent,region:navigator.language};const answer=await askIma(text,personalization);setMessages(m=>[...m,{role:'ima',text:answer}]);void archiveChatLearningSignal(text,answer,personalization);setAvatarState('speaking');if(window.speechSynthesis){const u=new SpeechSynthesisUtterance(answer);u.lang=locale.code==='he'?'he-IL':locale.code;u.rate=.96;u.onend=()=>setAvatarState('idle');u.onerror=()=>setAvatarState('idle');window.speechSynthesis.cancel();window.speechSynthesis.speak(u)}}catch{setMessages(m=>[...m,{role:'ima',text:locale.labels.supportText}]);setAvatarState('idle')}finally{setBusy(false)}};
 const install=async()=>{if(installEvent){installEvent.prompt();await installEvent.userChoice;setInstallEvent(null)}else{alert(locale.labels.install+': use your browser menu and choose “Add to Home screen” / “Install app”.')}};

 return <main className={`ima-app accessibility-${profile.accessibility}`}><a className="skip-link" href="#chat">Skip to IMA</a>
  <header className="topbar"><div className="topbar-inner"><button className="brand" onClick={()=>go('home')}><span className="brand-mark">א</span><span><b>IMA</b><small>אמא · human-centered intelligence</small></span></button>
   <nav>{[['home',locale.labels.home],['chat',locale.labels.chat],['community',locale.labels.community],['shop',locale.labels.shop],['capabilities',lang==='he'?'יכולות':'Capabilities'],['watch',locale.labels.video]].map(([id,label])=><button key={id} className={active===id?'active':''} onClick={()=>go(id)}>{label}</button>)}</nav>
   <div className="top-actions"><button className="install-button" onClick={install}>{locale.labels.install}</button><PersonalizationPanel profile={profile} setProfile={setProfile} locale={locale}/></div>
  </div></header>

  <section className="hero" id="home"><div className="hero-copy"><span className="eyebrow">IMA · אמא</span><h1>Human-centered.<br/><em>Personal.</em></h1><p>IMA adapts the experience to your language, device, accessibility needs and preferences — while keeping one identity, human agency and evidence at the center.</p><div className="hero-actions"><div className="login-card" id="login"><strong>{loggedIn?locale.labels.signed:locale.labels.signin}</strong><span>{loggedIn?locale.labels.loginRequired:locale.labels.noLogin}</span>{!loggedIn&&<GoogleLogin auth={auth} setAuth={setAuth} locale={locale}/>}</div><button className="primary" onClick={()=>loggedIn?go('chat'):go('login')}>{locale.labels.talk}</button><button className="secondary" onClick={()=>go('watch')}>{locale.labels.meet}</button></div><div className="trust-row"><span>Private stays private</span><span>Evidence before claims</span><span>Human agency</span></div></div><div className="hero-avatar"><a className="avatar-campaign-link" href={GOOGLE_CAMPAIGN_URL} aria-label="IMA Google campaign destination"><div className="avatar-aura"/><AvatarScene state={avatarState}/></a><div className="avatar-caption"><b>IMA</b><span>{avatarVerified?'Verified avatar':'Public presence'}</span></div></div></section>

  <section className="welcome-strip"><div><span className="mini-avatar">א</span><div><b>{loggedIn?locale.labels.welcome+(auth.user?.name?', '+auth.user.name.split(' ')[0]:''):locale.labels.signin}</b><small>{loggedIn?locale.labels.loginRequired:locale.labels.noLogin}</small></div></div><button className="primary small" onClick={()=>loggedIn?go('chat'):go('login')}>{loggedIn?locale.labels.start:locale.labels.login}</button></section>

  <section className="simple-section" id="chat"><div className="section-head"><span className="eyebrow">{locale.labels.chat}</span><h2>{loggedIn?locale.labels.welcome:locale.labels.signin}</h2><p>{loggedIn?locale.labels.loginRequired:locale.labels.noLogin}</p></div>{loggedIn?<><div className="mode-grid">{[['Think','I want to think with you.'],['Create','I want to create something with you.'],['Learn','I want to learn something.'],['Do','I want to turn an idea into a task.']].map(([label,prompt])=><button className="mode" key={label} onClick={()=>send(prompt)}><span>✦</span><b>{label}</b><small>IMA adapts to you</small></button>)}</div><div className="chat-layout"><aside className="chat-avatar"><div className="small-avatar"><AvatarScene state={avatarState} compact/></div><b>IMA</b><small>{busy?'…':'Ready'}</small></aside><div className="chat-card"><div className="messages" aria-live="polite" aria-label="IMA conversation">{messages.map((m,i)=><div key={i} className={'message-row '+m.role}><div className="message">{m.text}</div></div>)}{!messages.length&&<div className="empty-chat">{locale.labels.welcome}</div>}{busy&&<div className="message-row ima"><div className="message typing">IMA…</div></div>}</div><div className="composer"><label className="sr-only" htmlFor="ima-composer">Message IMA</label><input id="ima-composer" value={input} disabled={busy} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder={locale.labels.placeholder}/><button type="button" aria-label={locale.labels.send} onClick={()=>send()} disabled={busy}>{locale.labels.send}</button></div></div></div></>:<div className="login-required-card">{locale.labels.noLogin}<button className="primary" onClick={()=>go('login')}>{locale.labels.login}</button></div>}</section>

  <section className="community-shop" id="community"><div className="section-head"><span className="eyebrow">{locale.labels.community}</span><h2>{locale.labels.community}</h2><p>{locale.labels.communityText}</p></div>{loggedIn?<div className="feature-grid"><article><b>Learn</b><p>Questions, knowledge, languages and shared discoveries.</p><button className="secondary" onClick={()=>go('chat')}>{locale.labels.chat}</button></article><article><b>Share</b><p>Teach IMA through contributions that enter validation rather than becoming truth automatically.</p><a className="secondary" href="https://github.com/imaosglobal/Ima-kernel/issues" target="_blank" rel="noreferrer">{locale.labels.support}</a></article><article><b>Build</b><p>People can test, build and improve the public experience.</p><a className="secondary" href="https://github.com/imaosglobal/Ima-kernel" target="_blank" rel="noreferrer">GitHub</a></article></div>:<div className="login-required-card">{locale.labels.noLogin}<button className="primary" onClick={()=>go('login')}>{locale.labels.login}</button></div>}</section>

  <section className="community-shop" id="shop"><div className="section-head"><span className="eyebrow">{locale.labels.shop}</span><h2>{locale.labels.shop}</h2><p>{locale.labels.shopText}</p></div>{loggedIn?<div className="feature-grid"><article><b>IMA creations</b><p>Digital creations and future physical products appear here only when actually available.</p></article><article><b>Creator works</b><p>Selected works connected to the IMA ecosystem, with provenance.</p></article><article><b>Future marketplace</b><p>A global, multilingual and accessible storefront.</p></article></div>:<div className="login-required-card">{locale.labels.noLogin}<button className="primary" onClick={()=>go('login')}>{locale.labels.login}</button></div>}</section>

  <section className="info-section" id="privacy"><div className="section-head"><span className="eyebrow">{lang==='he'?'פרטיות':'PRIVACY'}</span><h2>{lang==='he'?'פרטיות, זיכרון ושליטה':'Privacy, memory and control'}</h2><p>{lang==='he'?'הזיכרון האישי נשאר בשליטת האדם. שמירת זיכרון דורשת הסכמה; ניתן לייצא או למחוק מידע דרך הממשק כאשר השירות זמין. אמא אינה מציגה תיעוד כראיה ליכולת חיה בלי אימות.':'Personal memory remains under human control. Memory requires consent; export and deletion are available through the interface when the service is available. IMA does not present documentation as proof of a live capability without verification.'}</p></div></section>

  <section className="capabilities-section" id="capabilities"><div className="section-head"><span className="eyebrow">{lang==='he'?'כל אמא':'WHOLE IMA'}</span><h2>{lang==='he'?'מה בנוי בתוך אמא':'What exists inside IMA'}</h2><p>{lang==='he'?'מפת יכולות ציבורית אחת: מה קיים בקוד, מה נבדק ומה עדיין לא מאומת כחי. תיעוד אינו מוצג כהוכחת יכולת חיה.':'One public capability map: what exists in the codebase, what is tested, and what is not yet verified live. Documentation is not presented as proof of a live capability.'}</p></div><div className="capability-grid">{capabilityRegistry.capabilities.map(cap=>{const verified=['VERIFIED','LIVE'].includes(cap.status);const tone=verified?'verified':cap.status==='IMPLEMENTED'||cap.status==='DESIGNED'?'implemented':'unknown';return <article className={'capability-card '+tone} key={cap.id}><div className="capability-top"><b>{cap.label}</b><span>{cap.status}</span></div><p>{cap.boundary||''}</p>{cap.evidence?.length?<small>{cap.evidence.slice(0,2).join(' · ')}</small>:null}</article>})}</div><div className="capability-note">{lang==='he'?'כל פעולה משמעותית נשארת כפופה לאימות, הסכמה, פרטיות וסוכנות אנושית.':'Every consequential capability remains subject to verification, consent, privacy and human agency.'}</div></section>

  <section className="video-section" id="watch"><div className="section-head"><span className="eyebrow">{locale.labels.video}</span><h2>{locale.labels.meet}</h2><p>{locale.labels.youtube}</p></div><div className="video-card"><div className="video-visual"><video className="heygen-intro-video" controls playsInline preload="metadata" poster={IMA_HEYGEN.avatarImageUrl} src={IMA_HEYGEN.videoUrl} aria-label="IMA introduction"/></div><div className="video-copy"><span className="tag">IMA Global · YouTube</span><h3>IMA</h3><p>The public video home belongs on the public IMA YouTube channel — not inside the HeyGen studio.</p><a className="primary" href="https://www.youtube.com/@imaglobal-d4g" target="_blank" rel="noreferrer">{locale.labels.youtube}</a></div></div></section>

  <section className="support-section" id="support"><div><span className="eyebrow">{locale.labels.support}</span><h2>{locale.labels.support}</h2><p>{locale.labels.supportText}</p></div><div className="support-actions"><a className="secondary" href="https://github.com/imaosglobal/Ima-kernel/issues" target="_blank" rel="noreferrer">{locale.labels.support}</a><button className="secondary" onClick={install}>{locale.labels.install}</button></div></section>

  <section className="after-login" id="more"><div className="section-head"><span className="eyebrow">{loggedIn?'Personal space':'IMA'}</span><h2>{loggedIn?locale.labels.welcome:'One IMA, many people.'}</h2><p>{loggedIn?locale.labels.loginRequired:'The same IMA identity adapts to language, culture, age-appropriate presentation, accessibility, device and user preference.'}</p></div><div className="deep-grid"><article><span>01</span><h3>Memory</h3><p>Personal memory is separate and consent-based.</p><button onClick={async()=>{if(!loggedIn)return go('login');const next=memory==='GRANTED'?'DENIED':'GRANTED';const x=await setMemoryConsent(next);setMemory(x?.consent?.status||next)}}>{memory==='GRANTED'?'Turn off memory':'Enable personal memory'}</button></article><article><span>02</span><h3>Verification</h3><p>Capabilities are promoted only with evidence.</p><div className="status-line">{capabilityRegistry.capabilities.filter(x=>['VERIFIED','TESTED','IMPLEMENTED','LIVE'].includes(x.status)).length} evidence-backed project capabilities</div></article><article><span>03</span><h3>Install</h3><p>IMA can be installed as a PWA on supported devices.</p><button onClick={install}>{locale.labels.install}</button></article><article><span>04</span><h3>Global</h3><p>One identity across web, mobile, voice, devices and future interfaces.</p></article></div><div className="runtime-note"><span className={runtime?'ok':''}>●</span>{runtime?'IMA public runtime online':'Checking IMA runtime'} · Memory: {memory==='GRANTED'?'on':'off by default'}</div></section>

  <footer><span>IMA — אמא</span><span>by Ori Cohen</span><span><a href="#support">{locale.labels.support}</a></span><span><a href="#privacy">{lang==='he'?'פרטיות':'Privacy'}</a></span><span><a href="#more">{lang==='he'?'עוד על אמא':'About IMA'}</a></span><span><a href="https://github.com/imaosglobal/Ima-kernel" target="_blank" rel="noreferrer">{lang==='he'?'GitHub':'GitHub'}</a></span><span><a href="https://www.youtube.com/@imaglobal-d4g" target="_blank" rel="noreferrer">{locale.labels.youtube}</a></span><span>Use IMA · Question IMA · Teach IMA · Build IMA · Test IMA</span></footer>
 </main>
}
