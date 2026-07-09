while true; do
  echo "🧠 starting IMA server..."
  node server.js
  echo "⚠️ server crashed/restarted, restarting in 2s..."
  sleep 2
done
