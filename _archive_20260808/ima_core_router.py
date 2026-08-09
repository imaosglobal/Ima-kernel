import ima_core_runtime
import ima_system
import ima_brain
import ima_mom

class IMARouter:

    def __init__(self):
        self.runtime = ima_core_runtime.CORE

    def process(self,message):

        core = self.runtime.process(message)

        try:
            learning = ima_system
            core["system_connected"] = True
        except:
            core["system_connected"] = False

        try:
            core["brain_connected"] = True
            core["memory_layer"] = ima_brain.__name__
        except:
            core["brain_connected"] = False

        try:
            import ima_mom
            core["mother_connected"] = True
            core["mother_layer"] = ima_mom.__name__
        except Exception:
            core["mother_connected"] = False

        return core


ROUTER=IMARouter()


def ask(message):
    return ROUTER.process(message)
