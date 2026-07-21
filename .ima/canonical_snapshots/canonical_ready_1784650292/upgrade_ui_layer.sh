#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel/ima-ui"

echo "=== IMA UI UPGRADE ==="

mkdir -p "$ROOT/src/api"
mkdir -p "$ROOT/src/components"
mkdir -p "$ROOT/src/styles"

cat > "$ROOT/src/api/imaClient.js" <<'EOF'
const API="http://127.0.0.1:8080";

export async function askIMA(message){
  const r = await fetch(`${API}/ask`,{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body:JSON.stringify({message})
  });

  return await r.json();
}

export async function getHealth(){
  const r=await fetch(`${API}/health`);
  return await r.json();
}

export async function getReady(){
  const r=await fetch(`${API}/ready`);
  return await r.json();
}
EOF


cat > "$ROOT/src/components/Message.jsx" <<'EOF'
export default function Message({role,text}){

return (
<div className={"message "+role}>
<strong>{role==="ima"?"IMA":"אורי"}:</strong>
<div>{text}</div>
</div>
)

}
EOF


cat > "$ROOT/src/components/Chat.jsx" <<'EOF'
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
EOF



cat > "$ROOT/src/components/MemoryPanel.jsx" <<'EOF'
export default function MemoryPanel(){

return(
<div className="panel">

<h3>זיכרון IMA</h3>

<p>
מחובר לזיכרון המקומי:
</p>

<ul>
<li>memory.json</li>
<li>conversation layer</li>
<li>identity</li>
</ul>

</div>
)

}
EOF



cat > "$ROOT/src/App.jsx" <<'EOF'
import Chat from "./components/Chat";
import MemoryPanel from "./components/MemoryPanel";
import "./index.css";


export default function App(){

return(

<div className="app">

<header>

<div className="avatar">
<div className="pulse"></div>
</div>

<h1>IMA</h1>

<p>
מחפשת אמת דרך חיבור
<br/>
בין חוויה אישית,
יצירה ומערכות מורכבות
</p>

<button>
Mother Mode
</button>

</header>


<section className="dashboard">

<div className="card">
<h2>שיחה</h2>
<Chat/>
</div>


<div className="card">
<h2>זיכרון</h2>
<MemoryPanel/>
</div>


<div className="card">
<h2>מערכת</h2>

<p>
Runtime ✅
<br/>
Memory ✅
<br/>
Watchdog ✅
<br/>
API ✅
</p>

</div>

</section>

</div>

)

}
EOF



cat > "$ROOT/src/index.css" <<'EOF'
*{
box-sizing:border-box;
}

body{

margin:0;
font-family:
Arial,
sans-serif;

direction:rtl;

background:#10131a;
color:white;

}


.app{

min-height:100vh;
padding:30px;

}


header{

text-align:center;

}


.avatar{

width:120px;
height:120px;
margin:auto;
border-radius:50%;

background:
radial-gradient(circle,#fff,#8be9ff,#202040);

display:flex;
align-items:center;
justify-content:center;

animation:float 4s infinite;

}


.pulse{

width:40px;
height:40px;
border-radius:50%;
background:white;

animation:pulse 2s infinite;

}


.dashboard{

display:grid;

grid-template-columns:
repeat(auto-fit,minmax(280px,1fr));

gap:20px;

margin-top:40px;

}


.card{

background:#1b2130;
padding:20px;
border-radius:20px;

}


.message{

padding:10px;
margin:8px;
border-radius:12px;

}


.user{

background:#304060;

}


.ima{

background:#233b35;

}


.chat input{

width:70%;
padding:10px;

}


button{

padding:10px 20px;
border-radius:10px;
cursor:pointer;

}


@keyframes float{

50%{
transform:translateY(-10px);
}

}


@keyframes pulse{

50%{
transform:scale(1.3);
}

}

EOF



echo "=== UI UPGRADE COMPLETE ==="
echo "Run:"
echo "cd ima-ui && npm run dev"

