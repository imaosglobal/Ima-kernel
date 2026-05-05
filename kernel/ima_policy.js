
function allow(action){
  // דוגמה בסיסית — הרחב בהמשך
  const blocked = ['rm -rf', 'shutdown', 'reboot'];
  if(blocked.some(b => (action||'').includes(b))){
    return { ok:false, reason:'blocked action' };
  }
  return { ok:true };
}

module.exports = { allow };
