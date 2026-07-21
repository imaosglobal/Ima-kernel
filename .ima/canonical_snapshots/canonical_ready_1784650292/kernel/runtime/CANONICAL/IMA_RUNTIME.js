const state=require("./IMA_STATE")
const events=require("./IMA_EVENTS")
const heal=require("./IMA_HEAL")
const policy=require("./IMA_POLICY")

const runtime={

    boot(){
        state.set("status","ONLINE")

        events.emit(
            "BOOT",
            {
                time:Date.now()
            }
        )

        return {
            status:"ONLINE",
            heal:heal.check()
        }
    },

    state,
    events,
    heal,
    policy
}


if(require.main===module){
    console.log(JSON.stringify(runtime.boot(),null,2))
}

module.exports=runtime
