#!/data/data/com.termux/files/usr/bin/bash

# אם כבר בתוך ima_kernel - לא לעשות כלום
if [ "$(pwd)" = "$HOME/ima_kernel" ]; then
  return 0 2>/dev/null || exit 0
fi

cd "$HOME/ima_kernel" || exit 1
