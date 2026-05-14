module.exports = {

  auth(key){
    return key === "demo";
  },

  async run(task, data){

    if(!task) return "NO TASK";

    if(task === "hello"){
      return "IMA ALIVE";
    }

    if(task === "analyze"){
      return {
        insight: "basic analysis",
        input: data
      };
    }

    if(task === "generate"){
      return {
        output: "generated result",
        input: data
      };
    }

    return "UNKNOWN TASK";
  }

};

const PAID_KEYS = ["pro123"];

module.exports.auth = function(key){
  return key === "demo" || PAID_KEYS.includes(key);
};

const fs = require("fs");

function checkLimit(){
  let count = 0;
  try {
    count = parseInt(fs.readFileSync("calls.txt","utf8")) || 0;
  } catch(e){}

  count++;
  fs.writeFileSync("calls.txt", count.toString());

  console.log("CALL COUNT:", count);

  if(count > 2) return null; // disabled
  return null;
}

module.exports.limitCheck = checkLimit;
