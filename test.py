def cpreader(self):
    output = ''
    replace_dict = {"MN:": "MODEL:\t",
                    "BASE:": "BASE:\t",
                    "VER:": "VERSION:\t",
                    "HIDVER:": "DEVICE FIRMWARE\t",
                    "MNC:": "MNC:\t",
                    "MCC:": "MCC:\t",
                    "PRD:": "PRD:\t",
                    "AID:": "AID:\t",
                    "CC:": "CC:\t",
                    "OMCCODE:": "OMCCODE:\t",
                    "SN:": "SERIAL NUMBER:\t",
                    "IMEI:": "IMEI:\t",
                    "UN:": "UNIQUE ID:\t",
                    "PN:": "PN:\t",
                    "CON:": "USB CONNECTION:\t",
                    "LOCK:": "LOCK\t",
                    "LIMIT:": "LIMIT\t",
                    "SDP:": "SDP\t",
                    "HVID:\t": "DATA TREE:\t"}
    self.ui.logfield.append('reading in MTP Mode')
    info = detect.mode.Readmodem(detect.mode, detect.mode.samport(detect.mode))
    if info == ['']:
        info
        info
    for ifn in info:
        for dat in ifn:
            fida = dat.replace('(', ':\t').replace(')', "").replace('AT+DEVCONINFO', '').replace('+DEVCONINFO',
                                                                                                 '').replace('#OK#',
                                                                                                             '').replace(
                'OK', '')
            fida.replace(')', "")
            for key, value in replace_dict.items():
                fida = fida.replace(key, value)
            output += fida + "\n"
            self.ui.logfield.append(fida)
            self.ui.logfield.repaint()
    return output