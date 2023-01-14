class modelSelector:
    def __init__(self,model):
        self.model = model
        return (model)
    def modelXtics(cpu,efs,secEfs,nvdata,nvram,prt1,prt2):

        if cpu == "mtk":
             efs = 0;
             print(cpu, "the device doesnt reequire efs")
        else:
            print(f"the {cpu}device will require efs ")
        return(cpu)


a125f = modelSelector
a125f.modelXtics("mtk",0,0,0,0,0,0)
a127f = modelSelector
a127f.modelXtics("exynos",0,0,0,0,0,0)