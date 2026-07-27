from learning.runtime_bridge import emit_learning_event

def send_to_kernel(event):

    return {
        "bridge":"founder_kernel",
        "event":event
    }

