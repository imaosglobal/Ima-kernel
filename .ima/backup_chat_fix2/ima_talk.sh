#!/data/data/com.termux/files/usr/bin/bash
echo "=== מדבר עם אמא ==="
echo "כתוב exit ליציאה"
echo "לשליחת קובץ: כתוב FILE בהתחלה, כתוב END בסוף"
buffer=""; collecting=0
while true; do
    echo -n "אתה: "
    read -r line
    [ "$line" = "exit" ] && break
    
    if [ "$line" = "FILE" ]; then 
        collecting=1; buffer=""; echo "...שולח קובץ. סיים עם END"
        continue
    fi
    
    if [ "$line" = "END" ] && [ "$collecting" = "1" ]; then
        collecting=0
        json=$(python3 -c "import json; print(json.dumps({'text':'$buffer'}, ensure_ascii=False))")
        curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "$json"
        echo ""
        buffer=""; continue
    fi
    
    if [ "$collecting" = "1" ]; then 
        buffer="$buffer"$'\n'"$line"; continue
    fi
    
    json=$(python3 -c "import json; print(json.dumps({'text':'$line'}, ensure_ascii=False))")
    curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "$json"
    echo ""
done
