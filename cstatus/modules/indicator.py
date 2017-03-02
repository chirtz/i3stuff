from modules.modules import BasicModule
from tools import Tools
from modules.ipcserver import IPCServer


class Indicator(BasicModule, IPCServer):
    """
    Indicator Module
    Shows a circle with user-definable color, changeable via the given
    local socket port
    Example:
        Use the following in the console to set the color to green when the server port is 8080
        $   echo "#00ff00" | netcat localhost 8080
    """

    defaults = {
        "inactive_color": "#000000",
        "circle": Tools.sym("")
    }

    def __init__(self, template=defaults["circle"], color="#000000", port=8080, **kwargs):
        BasicModule.__init__(self, template=template, color=color, **kwargs)
        IPCServer.__init__(self, port=port)

    def clicked(self, button, *_):
        if button == 1:
            self.set_color("#ff0000")
        else:
            self.set_color("#ffffff")

    def on_recv(self, data):
        if len(data) == 7 and data.startswith("#"):
            self.set_color(data)

    def pre_output(self):
        if self.get_color() == self.values["inactive_color"]:
            self.active = False
        else:
            self.active = True

    def stop(self):
        pass







