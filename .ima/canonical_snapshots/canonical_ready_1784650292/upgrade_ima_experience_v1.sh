#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA EXPERIENCE LAYER V1 ==="

cd ~/ima_kernel/ima-ui

mkdir -p src/components/avatar
mkdir -p src/components/dashboard
mkdir -p src/styles
mkdir -p src/state

cat > src/state/imaPersona.js <<'EOF'
export const IMA_PERSONA = {
 name:"IMA",
 mode:"human",
 avatar:{
  type:"adaptive",
  source:null,
  animation:true,
  threeD:false
 },
 languages:["he","en","ar"],
 capabilities:[
  "conversation",
  "memory",
  "creation",
  "learning",
  "technology"
 ]
};
EOF


cat > src/components/avatar/IMAAvatar.jsx <<'EOF'
export default function IMAAvatar(){

return(
<div className="ima-avatar">

<div className="core">
</div>

</div>
)

}
EOF


cat > src/components/dashboard/Dashboard.jsx <<'EOF'
import Chat from "../Chat";
import MemoryPanel from "../MemoryPanel";
import IMAAvatar from "../avatar/IMAAvatar";


export default function Dashboard(){

return(
<div className="ima-dashboard">

<section className="hero">

<IMAAvatar/>

<h1>IMA</h1>

<p>
מחפשת אמת דרך חיבור
<br/>
בין חוויה אישית,
יצירה ומערכות מורכבות
</p>

</section>


<div className="modules">

<div className="module">
<h2>שיחה</h2>
<Chat/>
</div>


<div className="module">
<h2>זיכרון</h2>
<MemoryPanel/>
</div>


<div className="module">
<h2>מערכת</h2>

<p>
Runtime ✅
<br/>
Memory ✅
<br/>
Watchdog ✅
<br/>
Learning Layer ✅
<br/>
Device Layer ✅
</p>

</div>


</div>

</div>
)

}
EOF


cat > src/App.jsx <<'EOF'
import Dashboard from "./components/dashboard/Dashboard";
import "./index.css";

export default function App(){

return(
<Dashboard/>
)

}
EOF


cat >> src/index.css <<'EOF'


body{
background:
radial-gradient(circle at top,#26354f,#05070d);
font-family:
"Arial",
sans-serif;
}


.ima-dashboard{
min-height:100vh;
padding:40px;
}


.hero{
text-align:center;
}


.ima-avatar{

width:180px;
height:180px;

margin:auto;

border-radius:50%;

background:
linear-gradient(
135deg,
#ffffff,
#78e8ff,
#6b4cff
);

display:flex;
align-items:center;
justify-content:center;

animation:
float 5s infinite;

box-shadow:
0 0 60px #78e8ff;

}


.core{

width:70px;
height:70px;

background:white;

border-radius:50%;

animation:pulse 3s infinite;

}


.modules{

display:grid;

grid-template-columns:
repeat(auto-fit,minmax(300px,1fr));

gap:25px;

margin-top:50px;

}


.module{

background:
rgba(255,255,255,0.08);

backdrop-filter:
blur(20px);

border-radius:30px;

padding:25px;

border:
1px solid rgba(255,255,255,.15);

}


@keyframes float{

50%{
transform:translateY(-15px);
}

}


@keyframes pulse{

50%{
transform:scale(1.2);
}

}

EOF


echo "=== EXPERIENCE LAYER INSTALLED ==="

echo "Run:"
echo "cd ~/ima_kernel/ima-ui && npm run dev"

