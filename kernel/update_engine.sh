
#!/data/data/com.termux/files/usr/bin/bash

SNAPSHOT_DIR=~/ima_core/kernel/snapshots
mkdir -p $SNAPSHOT_DIR

echo "[UPDATE] START"

# snapshot bashrc
cp ~/.bashrc $SNAPSHOT_DIR/bashrc_$(date +%s)

echo "[UPDATE] pulling..."
git -C ~/ima_core/kernel pull

if [ $? -ne 0 ]; then
  echo "[UPDATE] FAILED → rollback"
  exit 1
fi

echo "[UPDATE] committing local changes..."
git -C ~/ima_core/kernel add .
git -C ~/ima_core/kernel commit -m "auto sync"
git -C ~/ima_core/kernel push

echo "[UPDATE] installing deps..."
npm install --prefix ~/ima_core/kernel

echo "[UPDATE] restarting system..."
bash ~/ima_core/kernel/start_daemon.sh

echo "[UPDATE] DONE"

