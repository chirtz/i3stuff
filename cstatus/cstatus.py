#!/usr/bin/env python3
import time

import threading
import json
import sys
from gi.repository import GLib, GObject
from config import Config


class CStatus:
    """
    Main Class for the CStatus output
    """
    def __init__(self):
        self._module_map = dict()
        self._callbacks = []
        for c in Config.bar_items:
            # Start module threads
            c.start()
            # Make modules accessible via their name for click callbacks
            self._module_map[c.get_name()] = c
        t = threading.Thread(target=self._update, daemon=True)
        t.start()

    def register_callback(self, cb_func):
        """
        Adds a callback function for item clicks
        :param cb_func:
        """
        self._callbacks.append(cb_func)

    def item_clicked(self, name, button, x, y):
        """
        Called when an item is clicked, forwards the event to the
        target item
        :param name: name of the item
        :param button: which button was used to click: 1, 2, ...
        :param x: x coordinate of the click
        :param y: y coordinate of the click
        """
        try:
            self._module_map[name].clicked(button, x, y)
        except KeyError:
            pass

    @staticmethod
    def run():
        """
        Glib main loop to process commands (needed for DBUS stuff)
        :return:
        """
        GObject.threads_init()
        loop = GLib.MainLoop()
        loop.run()

    def _update(self):
        """
        Regularly outputs the status line
        :return:
        """
        active = True
        while active:
            try:
                output = []
                for c in Config.bar_items:
                    # pre_output for non-timed/non-thread (basic) modules
                    c.pre_output()
                    if c.active:
                        output.append(c.get_output())
                for cb in self._callbacks:
                    cb(output)
                # sleep
                time.sleep(Config.UPDATE_INTERVAL)
            except (KeyboardInterrupt, SystemExit):
                active = False
                for c in Config.bar_items:
                    c.stop()


def init_i3bar_connection(cstatus):
    """
    Prepares i3bar IO
    """
    # i3bar requires a version header
    # also activate click events
    header = {"version": 1, "click_events": True}
    print(json.dumps(header))
    # start of the infinite array of status lines
    print("[")

    def print_status(ou):
        print("%s," % json.dumps(ou))

    def i3bar_reader():
        while True:
            l = sys.stdin.readline()
            # strip the header of the input
            if l.startswith("[") or l.startswith(","):
                l = l[1:]
            if l.strip() == "":
                continue
            try:
                # read one input line from i3bar
                d = json.loads(l)
                # if an item was clicked...
                if "name" in d:
                    cstatus.item_clicked(d["name"], d["button"], d["x"], d["y"])
            except KeyError:
                pass

    cstatus.register_callback(print_status)
    t1 = threading.Thread(target=i3bar_reader, daemon=True)
    t1.start()


if __name__ == "__main__":
    status = CStatus()
    init_i3bar_connection(status)
    CStatus.run()


