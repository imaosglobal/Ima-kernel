#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA REAL AVATAR LAYER ==="

mkdir -p src/experience/assets

cat > src/experience/IMAAvatar.jsx <<'EOF'
import {useState} from "react";

export default function IMAAvatar(){

const [state,setState]=useState("idle");

return (

<div className={"ima-avatar-stage "+state}
onClick={()=>setState("listening")}>

<div className="avatar-frame">

<img
className="ima-avatar-image"
src="/ima-avatar.png"
alt="IMA"
/>

</div>

<div className="avatar-state">
{state==="idle" && "IMA"}
{state==="listening" && "מקשיבה"}
{state==="speaking" && "מדברת"}
</div>

</div>

)

}
EOF


cat >> src/index.css <<'EOF'

.ima-avatar-stage{

display:flex;
flex-direction:column;
align-items:center;
gap:15px;

}


.avatar-frame{

width:260px;
height:260px;

border-radius:50%;

overflow:hidden;

background:
radial-gradient(circle,#fff,#b8eaff,#766cff);

box-shadow:
0 0 80px rgba(120,220,255,.8);

}


.ima-avatar-image{

width:100%;
height:100%;

object-fit:cover;

}


.avatar-state{

font-size:20px;

}


.listening .avatar-frame{

transform:scale(1.05);

}


EOF


echo "=== DONE ==="
echo "Place avatar image:"
echo "public/ima-avatar.png"

