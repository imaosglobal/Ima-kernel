export default function Message({role,text}){

return (
<div className={"message "+role}>
<strong>{role==="ima"?"IMA":"אורי"}:</strong>
<div>{text}</div>
</div>
)

}
