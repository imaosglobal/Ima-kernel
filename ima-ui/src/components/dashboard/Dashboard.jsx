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
