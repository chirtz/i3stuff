#!/usr/bin/env python3
"""
The main class and start script for the CBar
"""
from tkinter import *
import threading
import configparser
import os
from enum import Enum


class ConnectionType(Enum):
    """
    We currently distinguish whether we get our workspace/desktop information
    through I3-IPC or XLib
    """
    I3 = 1
    X11 = 2


class CBar:

    i3_connection = None

    def __init__(self, config):
        """
        Initialize stuff
        :param config: config.ini parsed
        """
        self._config = config
        self._xconnector = XConnector()
        self._connection = None
        self._init_layout()
        if self._xconnector.get_wm_name() == "i3":
            self._init_i3_ipc()
        else:
            self._init_x11_ipc()

    def _init_layout(self):
        """
        Initializes the layout of the root and children views
        """
        self.root = Tk()
        self.root.wm_client("cbar")
        # uniform background color
        self.root["bg"] = self._config["Colors"]["bg_default"]
        self.root.resizable(width=False, height=False)
        # needed for top bar
        self.root.wm_attributes("-type", "dock")
        # other windows are always behind the bar
        self.root.wm_attributes("-topmost", True)
        # background for child elements
        self.root.option_add("*Background", self._config["Colors"]["bg_default"])

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Set width to screen width and height to minimal height given in config file
        if "bottom" in self._config["General"]["position"].lower():
            y_pos = self.root.winfo_screenheight()
        else:
            y_pos = 0
        self.root.wm_geometry("+0+%d" % y_pos)
        self.root.wm_minsize(self.root.winfo_screenwidth(), height=self._config.getint("General", "min_height"))

        # Initialize the workspace bar (left, shows workspace names/numbers)
        self._workspace_bar = WorkspaceBar(self.root, self._xconnector, self._config["Workspaces"],
                                           self._config["Colors"])
        # Initialize the status bar (right, shows status items)
        self._status_bar = StatusBar(self.root, self._config["Status"], self._config["Colors"])

    def _init_i3_ipc(self):
        """
        Initializes the IPC connection to i3
        """
        self._connection = ConnectionType.I3
        i3_thread = threading.Thread(daemon=True, target=self._i3_thread)
        i3_thread.start()

    def _i3_thread(self):
        """
        Thread running the main loop for the i3 IPC. In case the connection is lost, e.g. due to an i3 reload,
        wait a bit and try to establish the connection, again.
        """
        global i3_connection
        import i3ipc
        import time
        while True:
            try:
                i3_connection = i3ipc.Connection()
                i3_connection.on('workspace', self._workspace_bar.update_buttons_i3)
                i3_connection.on('mode', lambda _, x: print(x))
                # Initial workspace bar refresh
                self._workspace_bar.update_buttons_i3(i3_connection, None)
                print("i3 connected")
                i3_connection.main()
            except Exception as e:
                print(e)
            finally:
                print("i3 connection lost, retry...")
                time.sleep(1)

    def _init_x11_ipc(self):
        """
        Initializes the X11 connection
        """
        self._connection = ConnectionType.X11
        self._xconnector.add_change_listener(self._workspace_bar.update_buttons_standard)
        self._xconnector.start_listening()
        self._workspace_bar.update_buttons_standard()

    def mainloop(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:  # gracefully exit on Ctrl+C
            print("Exiting cbar...")
        finally:
            if self.i3_connection:
                self.i3_connection.main_quit()


if __name__ == "__main__":
    # CStatus needs to be in the PYTHONPATH
    p = os.path.dirname(os.path.realpath(__file__))
    # Remove this line and add cstatus to the PYTHONPATH variable
    sys.path.append("%s/../cstatus" % p)
    from status_bar import StatusBar
    from workspaces_bar import WorkspaceBar
    from xconnector import XConnector

    # read config file and pass it to the bar, then loop
    cnf = configparser.ConfigParser()
    cnf.read("%s/config.ini" % p)
    bar = CBar(cnf)
    import asyncore

    t1 = threading.Thread(target=asyncore.loop, daemon=True)
    t1.start()
    bar.mainloop()

