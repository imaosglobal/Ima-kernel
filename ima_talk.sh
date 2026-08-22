#!/data/data/com.termux/files/usr/bin/bash
cd ~/ima_kernel
CMD="$1"
shift
USER="${!#}" # המשתמש הוא תמיד המילה האחרונה
QUERY="${*:1:$#-1}" # כל מה שבאמצע זה השאילתה

if [[ "$CMD" == "חפש" ]]; then
elif [[ "$CMD" == "תהיי" ]]; then
  FORM="$1"
elif [[ "$CMD" == "דודל" ]]; then
else
  echo "פקודות: ima חפש [מילה] [שם] | ima תהיי [צורה] [שם] | ima דודל"
fi
