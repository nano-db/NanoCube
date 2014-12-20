import zmq


class Interface(object):
    def __init__(self, port):
        self.port = port

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:{0}".format(port))

    def start(self):
        while True:
            self._loop()

    def _loop(self):
        msg = self.socket.recv_json()
        cmd = msg.get('cmd')
        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            ret = self._not_found(cmd)
        else:
            ret = func(msg.get("data"))

        self.socket.send_json(ret)

    @staticmethod
    def _send_success(data):
        return {
            "status": "OK",
            "data": data
        }

    @staticmethod
    def _send_error(error):
        return {
            "status": "error",
            "error": error
        }

    def _not_found(self, cmd_name):
        return self.send_error("{} not found".format(cmd_name))