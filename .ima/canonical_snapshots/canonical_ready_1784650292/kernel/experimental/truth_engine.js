
module.exports={

score:function(sources){

if(!Array.isArray(sources)) return 0;

let score=0;

for(const s of sources){

if(
s &&
s.trusted
) score++;

}

return score/sources.length;

},

verify:function(values){

const map={};

for(const v of values){

map[v]=(map[v]||0)+1;

}

let best=null;
let max=0;

for(const k in map){

if(map[k]>max){

max=map[k];
best=k;

}

}

return {
value:best,
confidence:max/values.length
};

}

};
