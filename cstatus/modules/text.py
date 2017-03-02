from modules.modules import BasicModule
from modules.ipcserver import IPCServer


class SimpleText(BasicModule):
    """
    Simple Text Module
    Shows the given text
    """

    defaults = {
        "text": ""
    }

    def __init__(self, template="$text", **kwargs):
        super().__init__(template=template, **kwargs)

    def set(self, s):
        self.values["text"] = s


class InteractiveText(SimpleText, IPCServer):
    """
    Interactive Text Module
    Shows the given text. The text can furthermore be modified via a local socket
    Example:
        Use the following in the console to set the text to foo when the server port is set to 8080
        $   echo "foo" | netcat localhost 8080
    """

    def __init__(self, port=8081, **kwargs):
        SimpleText.__init__(self, **kwargs)
        IPCServer.__init__(self, port=port)

    def on_recv(self, data):
        self.set(data)





