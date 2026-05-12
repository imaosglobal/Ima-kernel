const listeners = {};

module.exports = {
  on(event, fn){
    listeners[event] = listeners[event] || [];
    listeners[event].push(fn);
  },

  emit(event, data){
    (listeners[event] || []).forEach(fn => fn(data));
  },

  list(){
    return Object.keys(listeners);
  }
};
