"use strict";
const innovation=require("./IMA_INNOVATION_LOOP.js");
const state={records:[],lessons:[]};
const MAX=500;
function ingest(input){
  const record=innovation.buildPathRecord(input);
  record.id=record.id||("path-"+Date.now()+"-"+(state.records.length+1));
  state.records.push(record); if(state.records.length>MAX) state.records.shift();
  if(record.outcome||record.evidence.length){
    state.lessons.push({id:record.id,principle:record.path[0]||null,evidence:record.evidence,outcome:record.outcome,privacy_classification:record.privacy_classification,confidence:record.confidence});
    if(state.lessons.length>MAX) state.lessons.shift();
  }
  return record;
}
function ingestSignal(signal){ return innovation.pathFromSignals([signal])[0] ? ingest(innovation.pathFromSignals([signal])[0]) : null; }
function teachBack(record){
  if(!record || record.privacy_classification==="PRIVATE") return {ok:false,reason:"private_path_not_transferable"};
  return {ok:true,pattern:record.path,guardrails:{privacy:record.reuse_scope,human_boundary:record.human_boundary,agency:record.agency_rule},evidence:record.evidence,confidence:record.confidence};
}
function status(){return {canonical:true,records:state.records.length,lessons:state.lessons.length,max:MAX,transfer_rule:"PRIVATE_EXPERIENCE -> VERIFIED_ABSTRACT_PRINCIPLE -> REUSABLE_PATTERN -> INDEPENDENTLY_TESTED_PATH"};}
module.exports={ingest,ingestSignal,teachBack,status,state};
