from modules.modules import ThreadModule
from pulsectl import Pulse
import os
from tools import Tools


class Volume(ThreadModule):
    defaults = {
        "icon_low": Tools.sym(""),
        "icon_high": Tools.sym(""),
        "icon_muted": Tools.sym("")
    }

    def __init__(self, sink_index=0, template="$icon $volume", interval=2, **kwargs):
        super().__init__(template, interval, **kwargs)
        self.pulse = Pulse()
        self.sink_index = sink_index

    def clicked(self, button, *_):
        if button == 1:
            os.system("pavucontrol")
        elif button == 4 or button == 5:
            sink = self.pulse.sink_list()[0]
            cur_volume = self.pulse.volume_get_all_chans(sink)
            if button == 4 and cur_volume < 1.0:
                self.pulse.volume_change_all_chans(sink, 0.05)
            elif cur_volume > 0.0:
                self.pulse.volume_change_all_chans(sink, -0.05)
            self._set_values()
            self.trigger_refresh()

    def _set_values(self):
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

    def repeat(self):
        self._set_values()

