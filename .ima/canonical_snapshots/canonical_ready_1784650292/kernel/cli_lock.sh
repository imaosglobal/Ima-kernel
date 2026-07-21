
FILE=~/.bashrc
HASH_FILE=~/ima_core/kernel/.cli_hash

calc() {
  sha256sum "$FILE" | awk '{print $1}'
}

check() {
  if [ -f "$HASH_FILE" ]; then
    OLD=$(cat $HASH_FILE)
    NEW=$(calc)

    if [ "$OLD" != "$NEW" ]; then
      echo "[CLI LOCK] WARNING: CLI CHANGED"
      return 1
    fi
  fi
  return 0
}

lock() {
  calc > "$HASH_FILE"
  echo "[CLI LOCK] CLI LOCKED"
}

case "$1" in
  lock) lock ;;
  check) check ;;
esac

