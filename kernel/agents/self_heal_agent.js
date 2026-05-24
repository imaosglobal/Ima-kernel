setInterval(async ()=>{

  try {

    const res = await fetch("http://localhost:7000/health")
    const json = await res.json()

    if(!json.ok){
      console.log("[AGENT] unhealthy")
    } else {
      console.log("[AGENT] stable")
    }

  } catch(e){
    console.log("[AGENT] recovery needed")
  }

},10000)
