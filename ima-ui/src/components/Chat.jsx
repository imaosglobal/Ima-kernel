import { ChatPanel } from "../App";

export default function Chat({ language = "he", user = null }) {
  return <ChatPanel lang={language} user={user} chatOnly />;
}
