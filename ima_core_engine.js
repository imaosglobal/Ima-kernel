class IMA {

  constructor({ memory, tools }) {
    this.memory = memory;
    this.tools = tools;
  }

  async ask(userId, input) {

    // 1. Load personal context
    const userMemory = this.memory.loadUser(userId);

    // 2. Get global patterns
    const globalContext = this.memory.getGlobal();

    // 3. Decide response
    const response = await this.reason(input, userMemory, globalContext);

    // 4. Store interaction (with consent layer assumed)
    this.memory.store(userId, input, response);

    return response;
  }

  async reason(input, userMemory, globalContext) {

    return {
      answer: `IMA response to: ${input}`,
      insights: globalContext.slice(-3),
      personal_context_used: userMemory.length
    };
  }
}

module.exports = IMA;
