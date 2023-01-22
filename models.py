import tkinter

import gui


class modelSelector:
    def __init__(self, model):
        self.model = model
        return (model)

    def modelXtics(cpu, efs, secEfs, nvdata, nvram, prt1, prt2):

        if cpu == "mtk":
            efs = 0;
            print(cpu, "the device doesnt reequire efs")
        else:
            print(f"the {cpu}device will require efs ")
        return (cpu)
