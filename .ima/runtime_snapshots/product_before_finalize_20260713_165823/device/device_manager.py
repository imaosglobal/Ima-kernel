class DeviceManager:
    def __init__(self):
        self.devices = []

    def register(self, device):
        self.devices.append(device)

    def list_devices(self):
        return self.devices
