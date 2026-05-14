const cluster = require('cluster');
const path = require('path');
const crypto = require('crypto');

const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');

const WORKERS = 2;

const STATE = {
  sessions: {}
};

function newSession(){
  const id = Date.now().toString();

  STATE.sessions[id] = {
    graph:{},
    executed:{},
    history:[],
    failed:false
  };

  return id;
}

function start(){

  if(cluster.isPrimary){

    const workerPath = path.join(
      __dirname,
      'KERNEL_CLUSTER_WORKER_BOOT.js'
    );

    cluster.setupPrimary({
      exec: workerPath
    });

    console.log('[MASTER] starting cluster:', WORKERS);

    for(let i=0;i<WORKERS;i++){

      const worker = cluster.fork({
        WORKER_ID:String(i)
      });

      worker.on('message',(msg)=>{

        const session = STATE.sessions[msg.session];

        if(!session) return;

        try{

          const res = EXEC.execute(msg.cmd);

          session.graph[msg.nodeId].status='done';

          session.graph[msg.nodeId].result=res;

          session.executed[msg.nodeId]=true;

          session.history.push({
            id:msg.nodeId,
            res
          });

        }catch(e){

          session.graph[msg.nodeId].status='failed';

          session.graph[msg.nodeId].error=e.message;

          session.failed=true;

        }

      });

    }

  }

}

function request(cmd){

  const sessionId = newSession();

  const nodeId = crypto
    .createHash('sha256')
    .update(JSON.stringify(cmd)+Date.now())
    .digest('hex');

  STATE.sessions[sessionId].graph[nodeId]={
    cmd,
    status:'queued'
  };

  const workers = Object.values(cluster.workers || {});

  const worker = workers[0];

  if(worker){

    worker.send({
      session:sessionId,
      nodeId,
      cmd
    });

  }

  return {
    session:sessionId,
    node:nodeId
  };

}

function inspect(sessionId){

  if(sessionId){
    return STATE.sessions[sessionId];
  }

  return STATE;

}

function metrics(){

  return {
    workers:Object.keys(cluster.workers || {}).length,
    sessions:Object.keys(STATE.sessions).length
  };

}

module.exports = {
  start,
  request,
  inspect,
  metrics
};


global.__WORKERS__ = global.__WORKERS__ || [];

const __originalFork = require('cluster').fork;

require('cluster').fork = function () {
  const w = __originalFork.apply(this, arguments);

  global.__WORKERS__.push(w);

  w.on('exit', () => {
    global.__WORKERS__ =
      global.__WORKERS__.filter(x => x.id !== w.id);
  });

  return w;
};

const __oldMetrics = module.exports.metrics;

module.exports.metrics = function () {
  const m = __oldMetrics ? __oldMetrics() : {};
  return {
    ...m,
    workers: global.__WORKERS__.length
  };
};
