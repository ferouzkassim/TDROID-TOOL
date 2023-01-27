import fastbootpy
from fastbootpy import *

for device in fastbootpy.FastbootManager.devices():
    print(device)

