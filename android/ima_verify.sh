#!/usr/bin/env bash

PKG="com.ima.core"

echo "[IMA] VERIFYING INSTALL"

if pm list packages | grep -q "$PKG"; then
  echo "[IMA] INSTALLED OK"
  am start -n "$PKG/.MainActivity" || echo "[IMA] FAILED TO START"
else
  echo "[IMA] NOT INSTALLED"
fi
