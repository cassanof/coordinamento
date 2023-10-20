import zmq
import time
import os
from typing import List, Literal, Dict, Optional, Tuple


class Node:
    def __init__(self, host="tcp://127.0.0.1:5555", sync="tcp://127.0.0.1:5556", idx: int = 0, num_nodes: int = 1):
        self.host = host
        self.idx = idx
        self.ctx = zmq.Context()
        self.num_nodes = num_nodes
        if self.idx == 0:
            self.pub_chan = self.ctx.socket(zmq.PUB)
            self.pub_chan.bind(self.host)
            self.sync_chan = self.ctx.socket(zmq.PULL)
            self.sync_chan.bind(sync)
        else:
            self.sync_chan = self.ctx.socket(zmq.PUSH)
            self.sync_chan.connect(sync)
            self.sub_chan = self.ctx.socket(zmq.SUB)
            self.sub_chan.connect(self.host)
            self.sub_chan.setsockopt_string(zmq.SUBSCRIBE, "")

    def sync_all(self):
        """
        Waits for everyone to sync up.
        """
        channel = "__sync__"
        if self.idx == 0:
            for _ in range(self.num_nodes - 1):
                self.sync_chan.recv()
            self.pub_chan.send_string(channel)
        else:
            # subscribe before sending sync
            self.sync_chan.send(b'')
            self.sub_chan.recv_string()
