class IMA_DEPLOYMENT_CORE_V1 {

constructor(){
this.name="IMA_DEPLOYMENT_CORE_V1";
this.status="active";
}

health(){
return {
deployment:this.name,
status:this.status
};
}

}

module.exports=IMA_DEPLOYMENT_CORE_V1;
