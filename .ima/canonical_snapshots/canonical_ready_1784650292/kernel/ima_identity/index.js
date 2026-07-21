module.exports = {
  login(provider, user){
    return {
      ok: true,
      provider,
      user,
      token: "ima_" + Date.now(),
    };
  },

  verify(token){
    return token && token.startsWith("ima_");
  }
};
