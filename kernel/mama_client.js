class MamaClient {
  constructor(apiKey, baseUrl = "http://localhost:4000") {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  async run(task) {
    const res = await fetch(this.baseUrl + "/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.apiKey
      },
      body: JSON.stringify({ task })
    });

    return await res.json();
  }

  async signup() {
    const res = await fetch(this.baseUrl + "/signup", {
      method: "POST"
    });

    return await res.json();
  }
}

module.exports = MamaClient;
