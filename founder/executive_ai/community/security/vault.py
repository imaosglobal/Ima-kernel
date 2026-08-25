from pathlib import Path
import json




    data={}

    if FILE.exists():
        data=json.loads(FILE.read_text())

    data[service]={
        "key":key,
        "enabled":True
    }

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(data,indent=2)
    )



    if FILE.exists():
        return json.loads(FILE.read_text()).get(service)

    return None
