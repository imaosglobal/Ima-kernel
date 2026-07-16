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
