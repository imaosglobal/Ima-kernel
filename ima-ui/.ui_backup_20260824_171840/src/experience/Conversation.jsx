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
