import fastbootpy as fb

class fboot:
    def __init__(self):
        pass

    def fbdevices(self):
        devs = fb.FastbootManager.devices()
        for dev in devs:
            pass
        return dev
    def flasher(self):
        dev = self.fbdevices(self)
        dev(fb.FastbootDevice.erase(self,'userdata'))
#