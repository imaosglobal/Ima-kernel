import { getSessionToken } from './imaChat';

const API_BASE=(import.meta.env.VITE_IMA_API_BASE||'https://ima-915m.onrender.com').replace(/\/$/,'');
const LOCAL='http://127.0.0.1:8787';

async function authHeaders(){
  let token=null;
  try { token=await getSessionToken(); } catch {}
  if (!token) { try { token=await getSessionToken(true); } catch {} }
  if (!token) throw new Error('Google/IMA session token unavailable; please sign in again');
  return {'Content-Type':'application/json','Authorization':`Bearer ${token}`};
}

async function localJson(path,options={}){
 const response=await fetch(LOCAL+path,{...options,headers:{'Content-Type':'application/json',...(options.headers||{})}});
 if(!response.ok)throw new Error(`local bridge HTTP ${response.status}`);
 return response.json();
}

export async function getLocalLiveBrowserStatus(){
 try{return await localJson('/status')}catch{return null}
}

export async function getLocalLiveBrowserScreenshot(){
 return localJson('/screenshot');
}

export async function localNavigate(url){return localJson('/navigate',{method:'POST',body:JSON.stringify({url})});}
export async function localTap(x,y){return localJson('/tap',{method:'POST',body:JSON.stringify({x,y})});}
export async function localEnroll(){const token=localStorage.getItem('ima-public-session-token');if(!token)throw new Error('IMA session required');return localJson('/enroll',{method:'POST',body:JSON.stringify({authorization:'Bearer '+token})});}
export async function localScroll(deltaX,deltaY,x=10,y=10){return localJson('/scroll',{method:'POST',body:JSON.stringify({deltaX,deltaY,x,y})});}
export async function localClick(selector){return localJson('/click',{method:'POST',body:JSON.stringify({selector})});}
export async function localType(text){return localJson('/type',{method:'POST',body:JSON.stringify({text})});}
export async function localKey(key){return localJson('/key',{method:'POST',body:JSON.stringify({key})});}

export async function createLiveBrowserSession(){
 const local=await getLocalLiveBrowserStatus();
 if(local?.ok)return {mode:'local-termux-chrome',sessionId:'local-termux-chrome',bridgeUrl:LOCAL,target:local.target,interactiveLiveViewUrl:null};
 const response=await fetch(API_BASE+'/ima-api/live-browser/session',{method:'POST',headers:await authHeaders(),body:'{}'});
 const data=await response.json().catch(()=>({}));
 if(!response.ok)throw new Error(data.error||`live browser HTTP ${response.status}`);
 return {...data,mode:data.mode||'remote-provider'};
}

export async function stopLiveBrowserSession(sessionId){
 if(!sessionId||sessionId==='local-termux-chrome')return {stopped:false,mode:'local-termux-chrome'};
 const response=await fetch(API_BASE+'/ima-api/live-browser/session/'+encodeURIComponent(sessionId),{method:'DELETE',headers:authHeaders()});
 const data=await response.json().catch(()=>({}));
 if(!response.ok)throw new Error(data.error||`live browser stop HTTP ${response.status}`);
 return data;
}
