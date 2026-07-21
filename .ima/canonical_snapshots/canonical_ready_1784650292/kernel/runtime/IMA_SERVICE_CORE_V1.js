const BUS = require('./KERNEL_EVENT_BUS_V2');

class IMAServiceCore {

    constructor(){
        this.name="IMA_SERVICE_CORE_V1";
        this.status="active";
    }


    health(){
        return {
            service:this.name,
            status:this.status
        };
    }


    handle(event){

        if(BUS && BUS.emit){
            BUS.emit(
                "ima.service.event",
                event
            );
        }

        return {
            received:true,
            event:event
        };
    }

}


module.exports = IMAServiceCore;
