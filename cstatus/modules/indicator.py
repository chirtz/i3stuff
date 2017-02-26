from modules.modules import BasicModule
from pydbus import SessionBus
from tools import Tools

class Indicator(BasicModule):
    """
      <node>
        <interface name='de.chirtz.i3bar.indicator'>
          <method name='indicate'>
          <arg type='s' name='a' direction='in'/>
          <arg type='s' name='response' direction='out'/>
          </method>
        </interface>
      </node>
    """

    defaults = {
        "inactive_color": "#000000",
        "circle": Tools.sym("")
    }

    def __init__(self, **kwargs):
        super().__init__(template=self.defaults["circle"], color="#000000", **kwargs)
        self.bus = SessionBus()
        for i in range(0, 5):
            try:
                self.obj = self.bus.publish("de.chirtz.i3bar.indicator%d" % i, self)
                break
            except RuntimeError:
                pass

    def clicked(self, button, *_):
        if button == 1:
            self.set_color("#ff0000")
        else:
            self.set_color("#ffffff")

    def pre_output(self):
        if self.get_color() == self.values["inactive_color"]:
            self.active = False
        else:
            self.active = True

    def stop(self):
        try:
            self.obj.unpublish()
        except NameError:
            pass

    def indicate(self, s):
        self.set_color(s)
        return s








