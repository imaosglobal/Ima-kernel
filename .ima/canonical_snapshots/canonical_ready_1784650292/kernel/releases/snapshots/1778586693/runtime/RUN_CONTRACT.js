module.exports = {
  singleProcess: true,
  entrypoint: "runtime/ENTRYPOINT.js",
  forbiddenPatterns: [
    "engine_v",
    "server.js",
    "autonomous_runtime_old"
  ]
};
