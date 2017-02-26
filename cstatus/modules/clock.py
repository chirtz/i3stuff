from modules.modules import ThreadModule
from datetime import datetime


class Clock(ThreadModule):
    """
    Clock Module
    Shows date and time
    """

    def __init__(self, template=None, interval=5, **kwargs):
        if template:
            t = template
        else:
            t = "$day.$month.$year $hour:$minute:$second"
        super().__init__(t, interval, **kwargs)

    def repeat(self):
        now = datetime.now()
        self.values["minute"] = "%02d" % now.minute
        self.values["hour"] = "%02d" % now.hour
        self.values["second"] = "%02d" % now.second
        self.values["year"] = now.year
        self.values["month"] = "%02d" % now.month
        self.values["day"] = "%02d" % now.day
        self.values["weekday"] = now.weekday()
