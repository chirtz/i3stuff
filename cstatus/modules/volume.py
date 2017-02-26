from modules.modules import BasicModule
from pulsectl import Pulse
import os
from tools import Tools


class Volume(BasicModule):
    defaults = {
        "icon_low": Tools.sym(""),
        "icon_high": Tools.sym(""),
        "icon_muted": Tools.sym("")
    }

    def __init__(self, sink_index=0, template="$icon $volume", **kwargs):
        super().__init__(template, **kwargs)
        self.pulse = Pulse()
        self.sink_index = sink_index

    def clicked(self, button, *_):
        if button == 1:
            os.system("pavucontrol")

    def pre_output(self):
        info = self.pulse.sink_info(self.sink_index)
        volume = int(self.pulse.volume_get_all_chans(info)*100)
        self.values["volume"] = volume
        if info.mute == 1:
            self.values["icon"] = self.values["icon_muted"]
            self.props["color"] = "#ff0000"
        else:
            self.props["color"] = "#ffffff"
            if volume < 30:
                self.values["icon"] = self.values["icon_low"]
            else:
                self.values["icon"] = self.values["icon_high"]

