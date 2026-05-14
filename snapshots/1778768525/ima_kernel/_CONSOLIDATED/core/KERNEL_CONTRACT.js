module.exports = {
  ENTRYPOINT: "runtime/ENTRYPOINT.js",
  SINGLE_PROCESS_ONLY: true,
  FORBIDDEN_PROCESSES: [
    "runtime/autonomous_runtime.js",
    "runtime/server.js"
  ]
};
