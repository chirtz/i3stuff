from tkinter import *
import cstatus


class StatusBar(Frame):
    """
    The Status bar
    """
    def __init__(self, parent, config, colors, column=1):
        super().__init__(parent)
        self._config = config
        self._colors = colors
        self._items = []
        self.grid(row=0, column=column, sticky=E)
        sep_spaces = self._config.getint("separator_spaces")
        separator_str = self._config.get("separator")
        self._separator_str = separator_str.center(len(separator_str) + 2 * sep_spaces)
        self._init_status_connection()

    def _init_status_connection(self):
        """
        Creates the status thread which outputs the status information
        :return:
        """
        self._cstatus = cstatus.CStatus()
        # Register callback for status updates
        self._cstatus.register_callback(self._update_status)

    def _update_status(self, status):
        """
        Called whenever the status is changed to update the visible status icons
        :param status: list of status item dicts
        """
        item_len = len(self._items)
        status_len = len(status)
        # Need #status_len buttons for the actual icons #status_len-1 buttons for the separators
        diff = status_len*2-1 - item_len
        # If the status input has increased, we need more labels
        if diff > 0:
            for x in range(0, diff):
                label = Label(self)
                label.bind("<Button-1>", self._status_clicked)
                label.bind("<Button-2>", self._status_clicked)
                label.bind("<Button-3>", self._status_clicked)
                label.bind("<Button-4>", self._status_clicked)
                label.bind("<Button-5>", self._status_clicked)
                label["font"] = self._config.get("font")
                label["fg"] = self._colors["fg_button"]
                self._items.append(label)
        else:  # If it has decreased, remove superfluous items from the grid
            for x in range(item_len, item_len+diff, -1):
                self._items[x].grid_remove()

        # And now update the contents!
        idx = 0
        for s in status:
            label = self._items[idx]
            label.grid(column=idx, row=0)
            label["text"] = s["full_text"]
            label["fg"] = s["color"]
            # Set a reference to the name of the status item as given by cstatus, so we can return
            # that information to cstatus if the item was clicked
            if "name" in s:
                label.__setattr__("cname", s["name"])

            idx += 1
            # No separator after last item
            if idx > item_len-1:
                break
            sep = self._items[idx]
            sep.grid(column=idx, row=0)
            sep["text"] = self._separator_str
            idx += 1

    def _status_clicked(self, event):
        """
        Callback for a clicked status item
        """
        if hasattr(event.widget, "cname"):
            self._cstatus.item_clicked(event.widget.cname, event.num, event.x, event.y)
