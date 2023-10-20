import argparse
import time
import random
import node

parser = argparse.ArgumentParser()
parser.add_argument('--role', type=str, default='follower')
parser.add_argument('--idx', type=int, required=True)
args = parser.parse_args()

node = node.Node(role=args.role)

while True:
    if random.random() < 0.1:
        print('| node {} is waiting'.format(args.idx))
        node.sync_all()
        print('+ node {} is done waiting'.format(args.idx))
    else:
        print('- node {} is working'.format(args.idx))
        time.sleep(0.1)
