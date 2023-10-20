import zmq
import time
import os
from typing import List, Literal, Dict, Optional, Tuple


class Node:
    def __init__(self, host="tcp://127.0.0.1:5555", sync="tcp://127.0.0.1:5556", idx: int = 0, num_nodes: int = 1):
        self.host = host
        self.idx = idx
        self.ctx = zmq.Context()
        self.sub_chans: Dict[str, zmq.Socket] = {}
        self.num_nodes = num_nodes
        if self.idx == 0:
            self.pub_chan = self.ctx.socket(zmq.PUB)
            self.pub_chan.bind(self.host)
            self.sync_chan = self.ctx.socket(zmq.PULL)
            self.sync_chan.bind(sync)
        else:
            self.sync_chan = self.ctx.socket(zmq.PUSH)
            self.sync_chan.connect(sync)

    def _get_sub_chan(self, channel: str) -> zmq.Socket:
        if channel not in self.sub_chans:
            sub_chan = self.ctx.socket(zmq.SUB)
            sub_chan.connect(self.host)
            sub_chan.setsockopt_string(zmq.SUBSCRIBE, channel)
            time.sleep(0.1)
            self.sub_chans[channel] = sub_chan

        return self.sub_chans[channel]

    def sync_all(self, channel=""):
        """
        Waits for everyone to sync up. You can specify a channel to sync on,
        or use the default channel.
        """
        channel = "__sync__{}".format(channel)
        if self.idx == 0:
            for _ in range(self.num_nodes - 1):
                print('waiting for sync')
                self.sync_chan.recv()
            print('sending pub')
            self.pub_chan.send_string(channel)
        else:
            # subscribe before sending sync
            sub_chan = self._get_sub_chan(channel)
            # recv and then wait 
            print('sending sync')
            self.sync_chan.send(b'')
            print('waiting for pub')
            sub_chan.recv()
