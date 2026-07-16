#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA IDENTITY LAYER V1 ==="

cd ~/ima_kernel/ima-ui

mkdir -p src/identity
mkdir -p src/components/avatar
mkdir -p src/components/layout


cat > src/identity/persona.json <<'EOF'
{
  "name":"IMA",
  "title":"מחפשת אמת דרך חיבור בין חוויה אישית, יצירה ומערכות מורכבות",
  "identity":"adaptive-human-interface",
  "avatar":{
    "type":"human",
    "mode":"adaptive",
    "threeDReady":true,
    "customizable":true
  },
  "languages":[
    "he",
    "en",
    "ar"
  ],
  "interface":{
    "rtl":true,
    "global":true
  }
}
EOF


cat > src/components/avatar/IMAAvatar.jsx <<'EOF'
import persona from "../../identity/persona.json";

export default function IMAAvatar(){

return (

<div className="ima-character">

<div className="face">

<div className="eye left"></div>
<div className="eye right"></div>

</div>

<div className="aura"></div>

</div>

)

}
EOF


cat > src/components/layout/IMAExperience.jsx <<'EOF'
import Chat from "../Chat";
import IMAAvatar from "../avatar/IMAAvatar";


export default function IMAExperience(){

return(

<div className="experience">


<header className="ima-header">

<IMAAvatar/>

<h1>IMA</h1>

<p>
מחפשת אמת דרך חיבור
<br/>
בין חוויה אישית,
יצירה ומערכות מורכבות
</p>

</header>


<section className="conversation">

<h2>שיחה עם IMA</h2>

<Chat/>

</section>


</div>

)

}
EOF


cat > src/App.jsx <<'EOF'
import IMAExperience from "./components/layout/IMAExperience";
import "./index.css";

export default function App(){

return <IMAExperience/>

}
EOF


cat >> src/index.css <<'EOF'


.experience{

min-height:100vh;

padding:40px;

direction:rtl;

}


.ima-header{

text-align:center;

}


.ima-character{

position:relative;

width:220px;

height:220px;

margin:auto;

display:flex;

align-items:center;

justify-content:center;

}


.face{

width:130px;

height:130px;

border-radius:50%;

background:
linear-gradient(
145deg,
#ffffff,
#b8e8ff,
#7770ff
);

position:relative;

z-index:2;

box-shadow:
0 0 60px rgba(120,220,255,.8);

animation:
float 5s infinite;

}


.eye{

position:absolute;

width:12px;

height:12px;

background:#222;

border-radius:50%;

top:55px;

}


.left{

right:40px;

}


.right{

left:40px;

}


.aura{

position:absolute;

width:210px;

height:210px;

border-radius:50%;

background:
radial-gradient(
circle,
transparent,
rgba(120,220,255,.35)
);

animation:pulse 4s infinite;

}


.conversation{

max-width:900px;

margin:40px auto;

background:
rgba(255,255,255,.08);

padding:30px;

border-radius:30px;

backdrop-filter:blur(20px);

}


@keyframes float{

50%{
transform:translateY(-15px);
}

}


@keyframes pulse{

50%{
transform:scale(1.15);
}

}

EOF


echo "=== IMA IDENTITY LAYER INSTALLED ==="
echo "Run:"
echo "cd ~/ima_kernel/ima-ui && npm run dev"

