import zmq

class Connector(object):
    def __init__(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:{0}".format(port))
        self.socket = socket

    @property
    def is_connected(self):
        try:
            self.socket.send("ping")
            ret = self.socket.recv()
        except zmq.error.ZMQError:
            return False
        else:
            return ret == "pong"
