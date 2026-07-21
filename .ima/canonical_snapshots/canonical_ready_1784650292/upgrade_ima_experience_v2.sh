#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA EXPERIENCE V2 ==="

cd ~/ima_kernel/ima-ui

mkdir -p src/experience/themes/warm
mkdir -p src/experience/themes/cosmic
mkdir -p src/experience/themes/custom


cat > src/experience/PersonaEngine.js <<'EOF'
export const PersonaEngine = {

name:"IMA",

presence:"warm",

identity:"adaptive-human",

appearance:{
type:"avatar",
mode:"customizable",
readyFor3D:true
},

language:{
rtl:true,
default:"he"
}

};
EOF


cat > src/experience/IMAAvatar.jsx <<'EOF'
import { PersonaEngine } from "./PersonaEngine";

export default function IMAAvatar(){

return (

<div className="ima-person">

<div className="hair"></div>

<div className="face">

<div className="eyes">
<span></span>
<span></span>
</div>

<div className="smile"></div>

</div>

<div className="light"></div>

</div>

)

}
EOF


cat > src/experience/Conversation.jsx <<'EOF'

export default function Conversation(){

return (

<div className="conversation">

<div className="ima-message">

שלום, אני IMA.
<br/>
אני כאן לשיחה, יצירה ולמידה.

</div>


<div className="input-area">

<input placeholder="כתוב הודעה ל-IMA..." />

<button>
שלח
</button>

</div>

</div>

)

}

EOF


cat > src/experience/IMAWorld.jsx <<'EOF'

import IMAAvatar from "./IMAAvatar";
import Conversation from "./Conversation";


export default function IMAWorld(){

return (

<div className="ima-world">


<section className="presence">

<IMAAvatar/>

<h1>IMA</h1>

<p>
מחפשת אמת דרך חיבור
<br/>
בין חוויה אישית,
יצירה ומערכות מורכבות
</p>

</section>


<Conversation/>


</div>

)

}

EOF


cat > src/App.jsx <<'EOF'

import IMAWorld from "./experience/IMAWorld";
import "./index.css";


export default function App(){

return <IMAWorld/>

}

EOF


cat >> src/index.css <<'EOF'


.ima-world{

min-height:100vh;

direction:rtl;

padding:30px;

background:
radial-gradient(
circle at top,
#344d70,
#080b12
);

color:white;

}


.presence{

text-align:center;

}


.ima-person{

width:260px;

height:260px;

margin:auto;

position:relative;

}


.face{

position:absolute;

width:150px;

height:150px;

left:55px;

top:60px;

border-radius:50%;

background:
linear-gradient(
145deg,
#fff,
#ffd9c7,
#8fdcff
);

z-index:2;

box-shadow:
0 0 50px rgba(150,220,255,.8);

}


.hair{

position:absolute;

width:170px;

height:100px;

left:45px;

top:35px;

border-radius:90px 90px 20px 20px;

background:#3b2630;

z-index:3;

}


.eyes{

display:flex;

justify-content:space-around;

padding-top:65px;

}


.eyes span{

width:14px;

height:14px;

background:#222;

border-radius:50%;

}


.smile{

width:45px;

height:20px;

border-bottom:3px solid #555;

border-radius:50%;

margin:20px auto;

}


.light{

position:absolute;

inset:0;

border-radius:50%;

background:
radial-gradient(
circle,
transparent,
rgba(120,220,255,.4)
);

animation:glow 4s infinite;

}


.conversation{

max-width:700px;

margin:40px auto;

padding:30px;

background:
rgba(255,255,255,.1);

border-radius:30px;

backdrop-filter:blur(20px);

}


.ima-message{

font-size:20px;

line-height:1.8;

}


.input-area{

margin-top:25px;

display:flex;

gap:10px;

}


.input-area input{

flex:1;

padding:15px;

border-radius:20px;

border:none;

}


.input-area button{

padding:15px 25px;

border-radius:20px;

border:none;

}


@keyframes glow{

50%{
transform:scale(1.1);
opacity:.7;
}

}

EOF


echo "=== IMA EXPERIENCE V2 READY ==="
echo "Run:"
echo "cd ~/ima_kernel/ima-ui && npm run dev"

