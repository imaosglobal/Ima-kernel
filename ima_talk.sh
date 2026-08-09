#!/data/data/com.termux/files/usr/bin/bash
cd ~/ima_kernel
CMD="$1"
shift
USER="${!#}" # המשתמש הוא תמיד המילה האחרונה
QUERY="${*:1:$#-1}" # כל מה שבאמצע זה השאילתה

if [[ "$CMD" == "חפש" ]]; then
  python3 -c "import ima_master_runtime; print(ima_master_runtime.ima_profile.ima_search('$QUERY', '$USER'))"
elif [[ "$CMD" == "תהיי" ]]; then
  FORM="$1"
  python3 -c "import ima_master_runtime; print(ima_master_runtime.ima_profile.request_form_change('$USER', '$FORM'))"
elif [[ "$CMD" == "דודל" ]]; then
  python3 -c "import ima_master_runtime; d=ima_master_runtime.ima_profile.get_today_doodle(); print('הדודל של היום: ' + d['form'] + ' | סיבה: ' + d['reason'])"
else
  echo "פקודות: ima חפש [מילה] [שם] | ima תהיי [צורה] [שם] | ima דודל"
fi
