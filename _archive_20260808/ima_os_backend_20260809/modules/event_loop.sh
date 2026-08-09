event_loop() {
  while read -r event; do

    TYPE=$(echo "$event" | grep -o '"type":"[^"]*"' | cut -d':' -f2 | tr -d '"')
    NAME=$(echo "$event" | grep -o '"name":"[^"]*"' | cut -d':' -f2 | tr -d '"')

    case "$TYPE" in
      service.crash)
        log "crash detected: $NAME"
        restart_service "$NAME" "${PIDS_CMD[$NAME]}"
      ;;
      service.restart)
        restart_service "$NAME" "${PIDS_CMD[$NAME]}"
      ;;
    esac

  done < "$BUS_INBOX"
}
