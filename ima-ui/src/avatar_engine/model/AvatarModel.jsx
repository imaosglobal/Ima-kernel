
import { IMAIdentity } from "../identity/imaIdentity";
import { ExpressionEngine } from "../expressions/expressionEngine";


export default function AvatarModel(){

const state=ExpressionEngine.current;


return (

<div className={"ima-avatar "+state}>


<div className="avatar-placeholder">

<div className="avatar-glow"></div>


<div className="avatar-symbol">

IMA

</div>


</div>


</div>

)

}

