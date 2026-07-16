#!/data/data/com.termux/files/usr/bin/bash

echo "=== FIX IMA EXPERIENCE LAYER ==="

cat > src/experience/Conversation.jsx <<'JS'
import {useState,useEffect,useRef} from "react";
import {askIMA} from "../api/imaClient";

export default function Conversation(){

const [messages,setMessages]=useState([
{
role:"ima",
text:"שלום אורי. אני IMA. אני כאן לשיחה, יצירה ולמידה."
}
]);

const [input,setInput]=useState("");
const [loading,setLoading]=useState(false);
const bottomRef=useRef(null);

useEffect(()=>{
bottomRef.current?.scrollIntoView({
behavior:"smooth"
});
},[messages]);


async function send(){

if(!input.trim() || loading) return;

const text=input;

setMessages(m=>[
...m,
{role:"user",text}
]);

setInput("");
setLoading(true);

try{

const result=await askIMA(text);

setMessages(m=>[
...m,
{
role:"ima",
text:
result?.answer?.response ||
result?.response ||
"לא התקבלה תשובה"
}
]);

}catch(e){

setMessages(m=>[
...m,
{
role:"ima",
text:"שגיאת חיבור לליבה"
}
]);

}

setLoading(false);

}


return(
<div className="conversation">

<div className="messages">

{messages.map((m,i)=>

<div
key={i}
className={
m.role==="ima"
?"ima-message"
:"user-message"
}
>

{m.text}

</div>

)}

<div ref={bottomRef}/>

</div>


<div className="input-area">

<input
value={input}
placeholder="דבר/י עם IMA"
disabled={loading}
onChange={e=>setInput(e.target.value)}
onKeyDown={e=>{
if(e.key==="Enter") send()
}}
/>

<button
onClick={send}
disabled={loading}
>
{loading?"...":"שלח"}
</button>

</div>

</div>
)

}
JS


cat > src/experience/IMAAvatar.jsx <<'JS'
export default function IMAAvatar(){

return(

<div className="ima-avatar-real">

<div className="avatar-placeholder">
IMA
</div>

</div>

)

}
JS


cat >> src/index.css <<'CSS'

.conversation{
width:100%;
max-width:700px;
margin:auto;
}

.messages{
height:55vh;
overflow-y:auto;
padding:20px;
}

.input-area{
display:flex;
gap:10px;
width:100%;
box-sizing:border-box;
}

.input-area input{
flex:1;
min-width:0;
}

.input-area button{
width:80px;
flex-shrink:0;
}


.ima-avatar-real{
display:flex;
justify-content:center;
align-items:center;
}

.avatar-placeholder{
width:180px;
height:180px;
border-radius:50%;
display:flex;
align-items:center;
justify-content:center;
font-size:40px;
}

CSS


echo "=== DONE ==="
echo "Restart Vite:"
echo "npm run dev"

