const API="/ima-api";

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
