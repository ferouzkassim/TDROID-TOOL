import fastbootpy as fb

def fbdevices():
    fb.FastbootManager.devices()
    for dev in fb.FastbootManager.devices():
        pass
    return dev
