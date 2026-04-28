const fs = require("fs");

class Distribution {

  constructor(){
    this.users = this.load("users.json");
    this.referrals = this.load("referrals.json");
    this.analytics = this.load("analytics.json");
  }

  load(file){
    if(fs.existsSync(file)){
      return JSON.parse(fs.readFileSync(file));
    }
    return {};
  }

  save(file, data){
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
  }

  registerUser(id, source = "direct"){

    if(!this.users[id]){
      this.users[id] = {
        id,
        source,
        created: Date.now(),
        active: true
      };

      this.save("users.json", this.users);
    }

    return this.users[id];
  }

  trackUsage(userId, event){

    if(!this.analytics[userId]){
      this.analytics[userId] = [];
    }

    this.analytics[userId].push({
      event,
      time: Date.now()
    });

    this.save("analytics.json", this.analytics);
  }

  addReferral(referrer, newUser){

    if(!this.referrals[referrer]){
      this.referrals[referrer] = [];
    }

    this.referrals[referrer].push(newUser);

    this.save("referrals.json", this.referrals);
  }

  getStats(){
    return {
      users: Object.keys(this.users).length,
      referrals: Object.keys(this.referrals).length
    };
  }
}

module.exports = Distribution;
