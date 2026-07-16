
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

