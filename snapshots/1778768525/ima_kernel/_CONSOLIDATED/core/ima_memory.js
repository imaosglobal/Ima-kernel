class Memory {

  constructor(){
    this.users = {};
    this.global = [];
  }

  loadUser(userId){
    return this.users[userId] || [];
  }

  store(userId, input, output){

    if(!this.users[userId]){
      this.users[userId] = [];
    }

    this.users[userId].push({ input, output });

    // Global aggregation (anonymized pattern only)
    this.global.push({
      pattern: typeof input,
      timestamp: Date.now()
    });
  }

  getGlobal(){
    return this.global;
  }
}

module.exports = Memory;
