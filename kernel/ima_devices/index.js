module.exports = {
  register(device){
    return {
      device,
      mode:
        device === "watch" ? "minimal" :
        device === "ar" ? "spatial" :
        device === "fridge" ? "simple_ui" :
        "full_ui"
    };
  }
};
