from modules.modules import ThreadModule
from tools import Tools


class Battery(ThreadModule):
    """
    Battery Module
    Reads the power information from /sys/class
    """
    BAT_PREFIX = "/sys/class/power_supply"
    defaults = {
        "bat_empty": Tools.sym(""),
        "bat_quarter": Tools.sym(""),
        "bat_half": Tools.sym(""),
        "bat_three_quarters": Tools.sym(""),
        "bat_full": Tools.sym(""),
        "ac": Tools.sym("")
    }

    def __init__(self, bat_name="BAT0", **kwargs):
        super().__init__("$icon $battery_percent", interval=30, **kwargs)
        self.bat_name = bat_name

    def repeat(self):
        f1 = open("%s/%s/charge_full" % (self.BAT_PREFIX, self.bat_name))
        charge_full = f1.read()
        f1.close()
        f2 = open("%s/%s/charge_now" % (self.BAT_PREFIX, self.bat_name))
        charge_current = f2.read()
        f2.close()
        f3 = open("%s/%s/status" % (self.BAT_PREFIX, self.bat_name))
        status = f3.read().strip()
        f3.close()

        bat_percent = int(int(charge_current)*100/int(charge_full))
        self.values["battery_percent"] = bat_percent
        self.props["urgent"] = False
        if status == "Charging":
            self.values["icon"] = self.values["ac"]
            self.set_color("#ffa500")
        else:
            self.set_color("#00ff00")
            if bat_percent >= 95:
                self.values["icon"] = self.values["bat_full"]
                self.set_color("#00ff00")
            elif bat_percent >= 70:
                self.values["icon"] = self.values["bat_three_quarters"]
            elif bat_percent >= 30:
                self.values["icon"] = self.values["bat_half"]
            elif bat_percent >= 15:
                self.values["icon"] = self.values["bat_quarter"]
            else:
                self.set_color("#ff0000")
                self.values["icon"] = self.values["bat_empty"]
                self.props["urgent"] = True
