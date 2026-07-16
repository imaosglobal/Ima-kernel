import {useState} from "react";
import {askIMA} from "../api/imaClient";
import Message from "./Message";

export default function Chat(){

const [messages,setMessages]=useState([]);
const [input,setInput]=useState("");

async function send(){

if(!input)return;

const q=input;

setMessages(m=>[
...m,
{role:"user",text:q}
]);

setInput("");

const r=await askIMA(q);

setMessages(m=>[
...m,
{
role:"ima",
text:r.answer?.response || JSON.stringify(r)
}
]);

}


return(
<div className="chat">

<div className="messages">
{
messages.map((m,i)=>
<Message key={i}{...m}/>
)
}
</div>


<div className="input">
<input
value={input}
onChange={e=>setInput(e.target.value)}
placeholder="דברי עם IMA"
/>

<button onClick={send}>
שלח
</button>

</div>

</div>
)

}
