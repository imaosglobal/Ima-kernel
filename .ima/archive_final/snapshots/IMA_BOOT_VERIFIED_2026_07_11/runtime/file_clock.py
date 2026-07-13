import os
import time

def file_metadata(path):
    st = os.stat(path)
    return {
        "path": path,
        "size": st.st_size,
        "created": getattr(st, "st_ctime", time.time()),
        "modified": getattr(st, "st_mtime", time.time()),
        "accessed": getattr(st, "st_atime", time.time())
    }
