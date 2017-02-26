from Xlib import X, display
import Xlib.protocol.event
from threading import Thread


class XConnector:
    """
    Connects to the X server via Xlib
    """
    def __init__(self):
        self.display = display.Display()
        self.root = self.display.screen().root
        self.change_listeners = []

    def add_change_listener(self, cb_func):
        """
        Adds a callback function to be called when the workspace was switched
        :param cb_func:
        """
        self.change_listeners.append(cb_func)

    def start_listening(self):
        """
        Starts the listener thread for workspace changes
        """
        t = Thread(target=XConnector._monitor_thread, daemon=True, args=[self.change_listeners])
        t.start()

    def _send_event(self, ctype, data, mask=None):
        """
        Wraps and sends commands to the X server
        """
        data = (data+[0]*(5-len(data)))[:5]
        ev = Xlib.protocol.event.ClientMessage(window=self.root, client_type=ctype, data=(32, data))
        if not mask:
            mask = (X.SubstructureRedirectMask | X.SubstructureNotifyMask)
        self.root.send_event(ev, event_mask=mask)

    def get_wm_name(self):
        """
        Returns the name of the used window manager
        :return: window manager
        :rtype: str
        """
        return self.root.get_full_property(self.display.intern_atom("_NET_WM_NAME"), 0).value

    def switch_workspace(self, num):
        """
        Switches to the given workspace
        :param: num (0..x)
        :type num: int
        """
        num = max(0, num)
        self._send_event(self.display.intern_atom("_NET_CURRENT_DESKTOP"), [num, X.CurrentTime])
        self.display.flush()

    def _get_value(self, prop):
        return self.root.get_full_property(self.display.intern_atom(prop), 0).value[0]

    def get_current_workspace(self):
        """
        Returns the currently active workspace
        :return: current workspace number
        :rtype: int
        """
        return self._get_value("_NET_CURRENT_DESKTOP")

    def get_number_of_workspaces(self):
        """
        Returns the overall number of workspaces
        :return: num of workspaces
        :rtype: int
        """
        return self._get_value("_NET_NUMBER_OF_DESKTOPS")

    def get_workspace_names(self):
        """
        Returns the names of the workspaces, if available
        :return: list of workspace names
        :rtype: list of str
        """
        return self.root.get_full_property(self.display.intern_atom("_NET_DESKTOP_NAMES"), 0).value.split("\x00")[:-1]

    @staticmethod
    def _monitor_thread(change_listeners):
        dis = display.Display()
        root = dis.screen().root
        root.change_attributes(event_mask=Xlib.X.SubstructureNotifyMask)
        while True:
            evt = dis.next_event()
            print(evt)
            for cb in change_listeners:
                cb()

