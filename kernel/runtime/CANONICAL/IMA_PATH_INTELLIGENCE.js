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
function ingestRuntimeSnapshot(snapshot){\n  const s=snapshot||{};\n  const evidence=Object.keys(s).map(k=>({module:k,status:s[k]}));\n  return ingest({\n    goal:"Traverse the current canonical IMA runtime safely and preserve the verified path/evidence for the next iteration.",\n    current_state:"RUNTIME_SNAPSHOT",\n    path:["boot canonical runtime","collect subsystem status","verify evidence","preserve reusable lesson","measure next outcome"],\n    evidence:evidence,\n    outcome:"RUNTIME_SNAPSHOT_CAPTURED",\n    provenance:"kernel/runtime/CANONICAL/IMA_RUNTIME.js",\n    privacy_classification:"SYSTEM_METADATA",\n    reuse_scope:"CANONICAL_SYSTEM_LEARNING",\n    confidence:"RUNTIME_OBSERVED"\n  });\n}\nfunction teachBack(record){
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
    verified_options:merged.map(p=>"PR #"+p.number+":"+p.class),
    path:["PR provenance","capability classification","runtime/path evidence","teach-back only after verification"],
    evidence:["merged_pr_count:"+merged.length,"open_unmerged_count:"+proposed.length,"closed_unmerged_count:"+closedUnmerged.length],
    outcome:"SCANNED_AND_MAPPED",
    provenance:"core/PR_PATH_INTEGRATION_REGISTRY.json",
    privacy_classification:"PUBLIC",
    reuse_scope:"CANONICAL_CAPABILITY_PROVENANCE",
    confidence:"VERIFIED_FROM_GITHUB_STATE"
  });
  const capability_records=prs.map(p=>ingest({
    goal:"Preserve and reuse the engineering path represented by PR #"+p.number+" ("+p.class+").",
    current_state:p.status,
    blocker:p.status==="OPEN_UNMERGED"?{type:"UNMERGED_PR",number:p.number}:null,
    verified_options:p.status==="MERGED"?["PR #"+p.number+" is present on canonical main"]:[],
    path:["identify PR provenance","classify implementation state",p.status==="MERGED"?"use only verified main-branch capability":"keep as proposal/evidence only","measure outcome before transferable adoption"],
    evidence:["pr_number:"+p.number,"status:"+p.status,"class:"+p.class],
    outcome:p.status==="MERGED"?"MERGED_CAPABILITY_REGISTERED":"NOT_LIVE",
    provenance:"core/PR_PATH_INTEGRATION_REGISTRY.json",
    privacy_classification:"PUBLIC",
    reuse_scope:p.status==="MERGED"?"CANONICAL_CAPABILITY_PROVENANCE":"PROPOSAL_ONLY",
    confidence:"VERIFIED_FROM_GITHUB_STATE"
  }));
  return {record_id:record.id,merged:merged.length,proposed:proposed.length,closed_unmerged:closedUnmerged.length,capability_records:capability_records.length};
}
function status(){return {canonical:true,records:state.records.length,lessons:state.lessons.length,max:MAX,transfer_rule:"PRIVATE_EXPERIENCE -> VERIFIED_ABSTRACT_PRINCIPLE -> REUSABLE_PATTERN -> INDEPENDENTLY_TESTED_PATH"};}
module.exports={ingest,ingestSignal,ingestCapabilityMap,ingestRuntimeSnapshot,teachBack,status,state};
