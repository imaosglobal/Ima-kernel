export const IMA_PERSONA = {
  name: "IMA",
  mode: "human",
  avatar: {
    type: "adaptive",
    source: "/Ima-kernel/mother_character.glb",
    animation: true,
    threeD: true,
    animationMode: "procedural",
    states: ["idle", "listening", "thinking", "speaking"]
  },
  languages: ["he", "en", "ar"],
  capabilities: [
    "conversation",
    "memory",
    "creation",
    "learning",
    "technology"
  ]
};
