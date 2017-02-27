from tkinter import *


class WorkspaceBar(Frame):
    """
    The Workspaces bar
    """
    def __init__(self, parent, xconnector, config, colors, column=0):
        super().__init__(parent)
        self._xconnector = xconnector
        self._config = config
        self._colors = colors
        self._buttons = []
        self.grid(row=0, column=column, sticky=W)
        self._init_buttons()

    def _init_buttons(self):
        """
        Initializes the workspace buttons according to the config
        """
        for i in range(self._config.getint("max_workspaces")):
            label = Label(self)
            label.bind("<Button-1>", self._ws_clicked)
            label["relief"] = self._config["button_style"]
            label["borderwidth"] = self._config["button_border"]
            label["font"] = self._config.get("font")
            label["fg"] = self._colors["fg_button"]
            self.grid_columnconfigure(i, minsize=self._config.getint("button_min_width"))
            self._buttons.append(label)

    def update_buttons_standard(self):
        """
        Update workspace buttons according to info from the X server
        """
        num = self._xconnector.get_number_of_workspaces()
        names = self._xconnector.get_workspace_names()
        current = self._xconnector.get_current_workspace()
        # Remove buttons for unused workspaces
        for x in range(num-1, len(self._buttons)):
            self._buttons[x].grid_remove()
        # Update the button contents
        for x in range(num):
            label = self._buttons[x]
            try:
                label["text"] = names[x]
            except IndexError:
                label["text"] = str(x+1)
            label.grid(column=x, row=0, sticky=W+E)
            # Set workspace number for callback function on click
            label.__setattr__("wnum", x)
            # Highlight the current workspace
            if current == x:
                label["bg"] = self._colors["bg_selected"]
            else:
                label["bg"] = self._colors["bg_default"]

    def update_buttons_i3(self, ipc_conn, event):
        if not event or event.current:
            # Get workspaces from i3 IPC
            workspaces = ipc_conn.get_workspaces()
            for idx, ws in enumerate(workspaces):
                label = self._buttons[idx]
                label["text"] = ws["name"]
                label.grid(column=idx, row=0, sticky=W+E)
                label.__setattr__("wnum", idx)
                if ws["visible"]:
                    label["bg"] = self._colors["bg_selected"]
                elif ws["urgent"]:
                    label["bg"] = self._colors["bg_urgent"]
                else:
                    label["bg"] = self._colors["bg_default"]

            for x in range(len(workspaces), len(self._buttons)):
                self._buttons[x].grid_remove()

    def _ws_clicked(self, e):
        """
        Called when a workspace button is clicked
        """
        self._xconnector.switch_workspace(e.widget.wnum)
