
const http = require("http");

function get(path) {
  return new Promise((resolve) => {
    http.get(`http://localhost:4000${path}`, (res) => {
      let data = "";
      res.on("data", c => data += c);
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve({});
        }
      });
    }).on("error", () => resolve({}));
  });
}

module.exports = {
  health: () => get("/v2/health"),
  queue: () => get("/v2/queue")
};

