const app = require("./kernel/app");

app.get("/health",(req,res)=>{
  res.json({ ok:true, system:"IMA_CORE_SERVER" });
});

app.listen(7000, ()=>{
  console.log("[IMA CORE SERVER RUNNING]");
});
