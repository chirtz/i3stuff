from modules.modules import BasicModule
from pydbus import SessionBus


class Text(BasicModule):
    """
      <node>
        <interface name='de.chirtz.i3bar.text'>
          <method name='set'>
          <arg type='s' name='a' direction='in'/>
          </method>
        </interface>
      </node>
    """

    def __init__(self, text, **kwargs):
        super().__init__("$text", **kwargs)
        self.values["text"] = text
        self.bus = SessionBus()
        self.obj = self.bus.publish("de.chirtz.i3bar.text", self)

    def set(self, s):
        self.values["text"] = s





