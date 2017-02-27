from Xlib import X, display
import Xlib.protocol.event
from threading import Thread


class XConnector:
    """
    Connects to the X server via Xlib
    """
    def __init__(self):
        self._display = display.Display()
        self._root = self._display.screen().root
        self._change_listeners = []
        self._thread = None
        self._active = False

    def add_change_listener(self, cb_func):
        """
        Adds a callback function to be called when the workspace was switched
        :param cb_func:
        """
        self._change_listeners.append(cb_func)

    def start_listening(self):
        """
        Starts the listener thread for workspace changes
        """
        self._thread = Thread(target=self._monitor_thread, daemon=True)
        self._thread.start()
        self._active = True

    def stop_listening(self):
        """
        Stops the listener thread
        """
        if self._thread:
            self._active = False
            self._thread.join()

    def _send_event(self, ctype, data, mask=None):
        """
        Wraps and sends commands to the X server
        """
        data = (data+[0]*(5-len(data)))[:5]
        ev = Xlib.protocol.event.ClientMessage(window=self._root, client_type=ctype, data=(32, data))
        if not mask:
            mask = (X.SubstructureRedirectMask | X.SubstructureNotifyMask)
        self._root.send_event(ev, event_mask=mask)

    def get_wm_name(self):
        """
        Returns the name of the used window manager
        :return: window manager
        :rtype: str
        """
        return self._root.get_full_property(self._display.intern_atom("_NET_WM_NAME"), 0).value

    def switch_workspace(self, num):
        """
        Switches to the given workspace
        :param: num (0..x)
        :type num: int
        """
        num = max(0, num)
        self._send_event(self._display.intern_atom("_NET_CURRENT_DESKTOP"), [num, X.CurrentTime])
        self._display.flush()

    def _get_value(self, prop):
        return self._root.get_full_property(self._display.intern_atom(prop), 0).value[0]

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
        return self._root.get_full_property(self._display.intern_atom("_NET_DESKTOP_NAMES"), 0).value.split("\x00")[:-1]

    def _monitor_thread(self):
        dis = display.Display()
        root = dis.screen().root
        root.change_attributes(event_mask=Xlib.X.SubstructureNotifyMask)
        while self._active:
            evt = dis.next_event()
            if evt.type == 22 and evt.override == 1 and evt.width == 10:
                for cb in self._change_listeners:
                    cb()

