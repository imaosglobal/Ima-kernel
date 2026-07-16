
export const ExpressionEngine = {

states:{
idle:"idle",
smile:"smile",
listening:"listening",
thinking:"thinking",
speaking:"speaking"
},

current:"idle",


set(state){

if(this.states[state]){
this.current=state;
}

return this.current;

}

};

