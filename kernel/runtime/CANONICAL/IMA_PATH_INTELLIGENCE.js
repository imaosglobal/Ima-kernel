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
function ingestCapabilityMap(registry){
  const prs=Array.isArray(registry?.pull_requests)?registry.pull_requests:[];
  const merged=prs.filter(p=>p.status==="MERGED");
  const proposed=prs.filter(p=>p.status==="OPEN_UNMERGED");
  const closedUnmerged=prs.filter(p=>p.status==="CLOSED_UNMERGED");
  const record=ingest({
    goal:"Connect verified IMA capabilities and their provenance into one reusable path-intelligence surface.",
    current_state:"CANONICAL_MAIN",
    blocker:proposed.length?{type:"PROPOSED_WORK",count:proposed.length}:null,
    verified_options:merged.map(p=>`PR #${p.number}:${p.class}`),
    path:["PR provenance","capability classification","runtime/path evidence","teach-back only after verification"],
    evidence:[`merged_pr_count:${merged.length}`,`open_unmerged_count:${proposed.length}`,`closed_unmerged_count:${closedUnmerged.length}`],
    outcome:"SCANNED_AND_MAPPED",
    provenance:"core/PR_PATH_INTEGRATION_REGISTRY.json",
    privacy_classification:"PUBLIC",
    reuse_scope:"CANONICAL_CAPABILITY_PROVENANCE",
    confidence:"VERIFIED_FROM_GITHUB_STATE"
  });
  return {record_id:record.id,merged:merged.length,proposed:proposed.length,closed_unmerged:closedUnmerged.length};
}
function status(){return {canonical:true,records:state.records.length,lessons:state.lessons.length,max:MAX,transfer_rule:"PRIVATE_EXPERIENCE -> VERIFIED_ABSTRACT_PRINCIPLE -> REUSABLE_PATTERN -> INDEPENDENTLY_TESTED_PATH"};}
module.exports={ingest,ingestSignal,ingestCapabilityMap,teachBack,status,state};
