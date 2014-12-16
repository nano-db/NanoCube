import zmq

class Connector(object):
    def __init__(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:{0}".format(port))
        self.socket = socket

    @property
    def is_connected(self):
        payload = {
            "cmd": "ping"
        }
        try:
            self.socket.send_json(payload)
            ret = self.socket.recv_json()
        except zmq.error.ZMQError:
            return False
        else:
            return ret.get('status') == "OK"

    def send_command(self, cmd_name, data):
        payload = {
            "cmd": cmd_name,
            "data": data
        }
        try:
            self.socket.send_json(payload)
            ret = self.socket.recv_json()
        except zmq.error.ZMQError:
            return "Impossible to connect to NanocubeDB", None
        else:
            if ret['status'] == "error":
                return None, ret['error']
            else:
                return ret['data'], None

    def list_cubes(self):
        ret, err = self.send_command("list", None)
        if err:
            print(err)
            return None
        else:
            return ret

    def close_connection(self):
        self.socket.close()
