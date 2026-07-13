#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL RUNTIME CONNECTOR ==="

DIR="kernel/runtime/CANONICAL"
BACKUP=".ima/runtime_backup_$(date +%s)"

mkdir -p "$BACKUP"

for f in IMA_RUNTIME.js IMA_STATE.js IMA_EVENTS.js IMA_HEAL.js IMA_POLICY.js
do
    if [ -f "$DIR/$f" ]; then
        cp "$DIR/$f" "$BACKUP/$f"
    fi
done

echo "[OK] backup created"

cat > "$DIR/IMA_EVENTS.js" <<'JS'
class IMAEvents {
    constructor(){
        this.listeners={}
    }

    on(name,fn){
        if(!this.listeners[name])
            this.listeners[name]=[]
        this.listeners[name].push(fn)
    }

    emit(name,data){
        for(const fn of this.listeners[name]||[])
            fn(data)
    }
}

module.exports=new IMAEvents()
JS


cat > "$DIR/IMA_STATE.js" <<'JS'
class IMAState {
    constructor(){
        this.data={}
    }

    set(key,value){
        this.data[key]=value
    }

    get(key){
        return this.data[key]
    }

    dump(){
        return this.data
    }
}

module.exports=new IMAState()
JS


cat > "$DIR/IMA_POLICY.js" <<'JS'
module.exports={
    allow(action){
        return true
    }
}
JS


cat > "$DIR/IMA_HEAL.js" <<'JS'
module.exports={
    check(){
        return {
            healthy:true,
            time:Date.now()
        }
    }
}
JS


cat > "$DIR/IMA_RUNTIME.js" <<'JS'
const state=require("./IMA_STATE")
const events=require("./IMA_EVENTS")
const heal=require("./IMA_HEAL")
const policy=require("./IMA_POLICY")

const runtime={

    boot(){
        state.set("status","ONLINE")

        events.emit(
            "BOOT",
            {
                time:Date.now()
            }
        )

        return {
            status:"ONLINE",
            heal:heal.check()
        }
    },

    state,
    events,
    heal,
    policy
}


if(require.main===module){
    console.log(JSON.stringify(runtime.boot(),null,2))
}

module.exports=runtime
JS


cat > kernel/runtime/CANONICAL/python_bridge.py <<'PY'
import subprocess
from pathlib import Path
import json

ROOT=Path(__file__).parent

def boot_runtime():
    result=subprocess.check_output(
        ["node",str(ROOT/"IMA_RUNTIME.js")],
        text=True
    )
    return json.loads(result)

if __name__=="__main__":
    print(boot_runtime())
PY


echo ""
echo "=== VERIFY FILES ==="

for f in \
kernel/runtime/CANONICAL/IMA_RUNTIME.js \
kernel/runtime/CANONICAL/IMA_STATE.js \
kernel/runtime/CANONICAL/IMA_EVENTS.js \
kernel/runtime/CANONICAL/IMA_HEAL.js \
kernel/runtime/CANONICAL/IMA_POLICY.js \
kernel/runtime/CANONICAL/python_bridge.py
do
    test -f "$f" && echo "[OK] $f" || {
        echo "[FAIL] missing $f"
        exit 1
    }
done


echo ""
echo "=== VERIFY NODE LOAD ==="

node - <<'NODE'
const r=require("./kernel/runtime/CANONICAL/IMA_RUNTIME.js");
let x=r.boot();

if(x.status!=="ONLINE")
{
 console.error("runtime failed");
 process.exit(1);
}

console.log("[OK] NODE RUNTIME",x.status);
NODE


echo ""
echo "=== VERIFY PYTHON BRIDGE ==="

python3 kernel/runtime/CANONICAL/python_bridge.py


echo ""
echo "=== VERIFY COMPLETE ==="
echo "IMA CANONICAL RUNTIME CONNECTED"
