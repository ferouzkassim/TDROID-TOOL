import clr
samdll = 'daemon/sam.dll'
t1 = clr.AddReference('daemon/sam.dll')
print(t1)