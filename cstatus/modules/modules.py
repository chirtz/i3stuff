import threading
import string
from tools import Tools


class BasicModule:

    defaults = {}
    pos = 0

    def __init__(self, template, on_clicked=None, constants=None, color=None, active=True):
        self.values = dict(self.defaults)
        self.props = dict()
        if constants:
            self.values.update(constants)
        if Tools.I3:
            self.props["markup"] = "pango"
        self.template = string.Template(template)
        self.props["full_text"] = ""
        self.props["color"] = color if color else "#ffffff"
        self.active = active
        self._assign_name()
        if on_clicked:
            self.clicked = on_clicked

    def _assign_name(self):
        self.props["name"] = "%d_%s" % (BasicModule.pos, self.__class__.__name__.lower())
        BasicModule.pos += 1

    def get_name(self):
        return self.props["name"]

    def clicked(self, button, pos_x, pos_y):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def get_color(self):
        return self.props["color"]

    def set_color(self, color):
        self.props["color"] = color

    def pre_output(self):
        pass

    def get_output(self):
        self.props["full_text"] = self.template.safe_substitute(self.values).strip()
        return self.props


class ThreadModule(BasicModule):
    def __init__(self, template, interval=None, **kwargs):
        super().__init__(template, **kwargs)
        if interval:
            self.interval = interval
        else:
            self.interval = 0
        self._stop_signal = threading.Event()

    def start(self):
        t = threading.Thread(target=self._repeat)
        t.daemon = True
        t.start()

    def stop(self):
        self._stop_signal.set()

    def _repeat(self):
        self.repeat()
        while not self._stop_signal.wait(self.interval):
            self.repeat()

    def repeat(self):
        pass
