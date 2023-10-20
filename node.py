import zmq
import os
from typing import List, Literal, Dict, Optional, Tuple


class Node:
    def __init__(self, host="tcp://localhost:5555", idx: int = 0):
        self.host = host
        self.idx = idx
        self.ctx = zmq.Context()
        self.sub_chans: Dict[str, zmq.Socket] = {}
        if self.idx == 0:
            self.pub_chan = self.ctx.socket(zmq.PUB)
            self.pub_chan.bind(self.host)

    def _get_sub_chan(self, channel: str) -> zmq.Socket:
        if channel not in self.sub_chans:
            sub_chan = self.ctx.socket(zmq.SUB)
            sub_chan.connect(self.host)
            sub_chan.setsockopt_string(zmq.SUBSCRIBE, channel)
            self.sub_chans[channel] = sub_chan

        return self.sub_chans[channel]

    def sync_all(self, channel=""):
        """
        Waits for everyone to sync up. You can specify a channel to sync on,
        or use the default channel.
        """
        channel = "__sync__{}".format(channel)
        if self.idx == 0:
            self.pub_chan.send_string(channel)

        elif self.idx > 0:
            sub_chan = self._get_sub_chan(channel)
            sub_chan.recv_string()

    #  def fork(num: int):
