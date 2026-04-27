const express = require("express");
const { loadUsers, getUser, createUser, saveUsers } = require("./kernel/user_engine");
const { decide } = require("./kernel/brain_core");
const { dispatch } = require("./kernel/action_dispatcher");

const app = express();
app.use(express.json());

app.post("/ima/run", async (req, res) => {
  const { message, userId } = req.body;

  const users = loadUsers();

  let user = getUser(users, userId);

  if (!user) {
    user = createUser(users, userId);
  }

  const decision = decide(message, user);

  let actionResult = null;

  if (decision.actions.length > 0) {
    actionResult = await dispatch(decision.actions[0], { message });
  }

  user.memory.push({
    message,
    time: Date.now()
  });

  saveUsers(users);

  res.json({
    result: actionResult?.result || "IMA response",
    user,
    debug: decision
  });
});

app.listen(4000, () => {
  console.log("🌍 IMA MULTI-USER SYSTEM RUNNING ON 4000");
});
