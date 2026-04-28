module.exports = (kernel) => {
  kernel.register("learning", (input) => {
    return "📚 learning: " + input;
  });
};
