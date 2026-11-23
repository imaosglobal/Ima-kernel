import './PublicApp.css';
import React,{useEffect,useState} from 'react';
import {askIma,submitFeedback} from './services/imaChat';

const C={
he:{name:'אמא',label:'בינה אנושית',title:'מה קורה אצלך עכשיו?',sub:'אפשר פשוט לדבר. אמא עוזרת לחשוב, להבין, ליצור ולפתור — בלי שתצטרך להבין איך היא בנויה.',ph:'כתוב לאמא…',start:'דבר עם אמא',thinking:'אמא חושבת…',empty:'ספר לי מה קורה.',how:'פשוט לדבר. אמא עושה את השאר.',cards:[['לחשוב','לסדר מחשבה או החלטה'],['ללמוד','להבין משהו חדש'],['ליצור','לכתוב, לבנות או להמציא'],['לפתור','להתקדם בבעיה אמיתית']],feedback:'משהו לא עבד טוב? ספר לאמא.',send:'שליחה',thanks:'תודה. זה נכנס ללולאת השיפור של אמא.',footer:'אמא — בינה אנושית'},
en:{name:'IMA',label:'Human-centered intelligence',title:'What is happening for you right now?',sub:'Just talk. IMA helps you think, understand, create and solve — without requiring you to understand how it is built.',ph:'Talk to IMA…',start:'Talk to IMA',thinking:'IMA is thinking…',empty:'Tell me what is going on.',how:'Just talk. IMA handles the rest.',cards:[['Think','Untangle a thought or decision'],['Learn','Understand something new'],['Create','Write, build or invent'],['Solve','Move forward on a real problem']],feedback:'Something did not work well? Tell IMA.',send:'Send',thanks:'Thank you. It enters IMA’s improvement loop.',footer:'IMA — Human-centered intelligence'}
};
const LANG=[['he','עברית'],['en','English'],['ar','العربية'],['es','Español'],['fr','Français'],['de','Deutsch'],['pt','Português'],['ru','Русский'],['uk','Українська'],['hi','हिन्दी'],['zh','中文'],['ja','日本語'],['ko','한국어']];
const RTL=new Set(['he','ar']);
function initial(){const s=localStorage.getItem('ima-site-language');if(s)return s;const b=String(navigator.language||'en').split('-')[0];return LANG.some(x=>x[0]===b)?b:'en'}

export default function PublicApp(){
 const [lang,setLang]=useState(initial),[messages,setMessages]=useState([]),[input,setInput]=useState(''),[busy,setBusy]=useState(false),[feedback,setFeedback]=useState(''),[sent,setSent]=useState(false);
 const t=C[lang]||C.en;
 useEffect(()=>{localStorage.setItem('ima-site-language',lang);document.documentElement.lang=lang;document.documentElement.dir=RTL.has(lang)?'rtl':'ltr';document.title=lang==='he'?'אמא — בינה אנושית':'IMA — Human-centered intelligence'},[lang]);
 async function send(text=input){const v=String(text||'').trim();if(!v||busy)return;setInput('');setMessages(m=>[...m,{role:'user',text:v}]);setBusy(true);try{const r=await askIma(v,{language:lang,interface:'canonical-public',authenticated:false,device_locale:navigator.language||lang});setMessages(m=>[...m,{role:'ima',text:r}])}catch{setMessages(m=>[...m,{role:'ima',text:lang==='he'?'אין לי כרגע תשובה מאומתת. אני לא אמציא תשובה. אפשר לנסות שוב או לתת לי עוד הקשר.':'I do not have a verified answer right now. I will not invent one. Try again or give me more context.'}])}finally{setBusy(false)}}
 return <div className="ima-public">
  <header className="public-header"><a className="public-brand" href="/Ima-kernel/" aria-label="IMA"><span className="brand-orb">א</span><span><strong>{t.name}</strong><small>{t.label}</small></span></a><select value={lang} onChange={e=>setLang(e.target.value)} aria-label="Language">{LANG.map(x=><option key={x[0]} value={x[0]}>{x[1]}</option>)}</select></header>
  <main>
   <section className="public-hero"><div className="hero-orb" aria-hidden="true">א</div><span className="public-label">{t.label}</span><h1>{t.title}</h1><p>{t.sub}</p><button className="public-primary" onClick={()=>document.getElementById('ima-input')?.focus()}>{t.start}</button></section>
   <section className="public-chat" aria-label={t.name}><div className="chat-top"><strong>{t.name}</strong><span>{t.how}</span></div><div className="messages" aria-live="polite">{!messages.length&&<div className="empty">{t.empty}</div>}{messages.map((m,i)=><div key={i} className={'message '+m.role}><span>{m.text}</span></div>)}{busy&&<div className="message ima"><span>{t.thinking}</span></div>}</div><div className="composer"><textarea id="ima-input" value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()}}} placeholder={t.ph} aria-label={t.ph} rows="1"/><button onClick={()=>send()} disabled={!input.trim()||busy} aria-label={t.start}>↑</button></div></section>
   <section className="public-cards">{t.cards.map(([a,b])=><button key={a} onClick={()=>{setInput(a+': ');document.getElementById('ima-input')?.focus()}}><strong>{a}</strong><span>{b}</span></button>)}</section>
   <section className="public-feedback"><p>{t.feedback}</p><div><input value={feedback} onChange={e=>setFeedback(e.target.value)} placeholder={t.feedback}/><button disabled={!feedback.trim()||sent} onClick={async()=>{try{await submitFeedback('improvement',feedback,{language:lang,source:'canonical-public'});setFeedback('');setSent(true)}catch{}}}>{sent?'✓':t.send}</button></div>{sent&&<small>{t.thanks}</small>}</section>
  </main><footer><span>{t.footer}</span></footer>
 </div>
}