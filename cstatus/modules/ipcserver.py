import asyncore
import socket


class IPCServer(asyncore.dispatcher):

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("localhost", port))
        self.listen(5)
        self.handler = None

    def on_recv(self, data):
        raise NotImplementedError

    def handle_accept(self):
        c = self.accept()
        self.handler = Handler(c[0], self)
        #self.close()


class Handler(asyncore.dispatcher_with_send):
    def __init__(self, s, ipc_server):
        super().__init__(sock=s)
        self._server = ipc_server

    def handle_read(self):
        data = self.recv(1024)
        self._server.on_recv(data.decode("utf-8").strip())





