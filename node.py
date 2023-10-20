import zmq
from typing import List, Literal, Dict, Optional, Tuple

Role = Literal["leader", "follower"]


class Node:
    def __init__(self, host="tcp://localhost:5555", role: Role = "follower"):
        self.host = host
        self.role = role
        self.ctx = zmq.Context()
        self.sub_chans: Dict[str, zmq.Socket] = {}
        if self.role == "leader":
            self.pub_chan = self.ctx.socket(zmq.PUB)
            self.pub_chan.bind(self.host)

    def _get_sub_chan(self, channel: str) -> zmq.Socket:
        if channel not in self.sub_chans:
            sub_chan = self.ctx.socket(zmq.SUB)
            sub_chan.connect(self.host)
            sub_chan.setsockopt_string(zmq.SUBSCRIBE, channel)
            self.sub_chans[channel] = sub_chan

        return self.sub_chans[channel]

    def sync_all(self, channel="__sync__"):
        """
        Waits for everyone to sync up. You can specify a channel to sync on,
        or use the default channel.
        """
        if self.role == "leader":
            self.pub_chan.send_string(channel)
        elif self.role == "follower":
            sub_chan = self._get_sub_chan(channel)
            sub_chan.recv_string()
