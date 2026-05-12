
const agent = require('./ima_agent.js');
const heal = require('./ima_self_heal.js');

function tick(cmd){
  const plan = agent.plan(cmd);
  agent.execute(plan);

  const issues = heal.analyze();
  heal.fix(issues);
}

module.exports = { tick };
