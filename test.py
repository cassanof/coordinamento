import argparse
import time
import random
import node

parser = argparse.ArgumentParser()
parser.add_argument('--idx', type=int, required=True)
parser.add_argument('--nodes', type=int, required=True)
args = parser.parse_args()

node = node.Node(idx=args.idx, num_nodes=args.nodes)
time.sleep(1)
print('node {} is ready'.format(args.idx))
node.sync_all()

while True:
    r = random.random()
    if r < 0.1:
        print('| node {} is waiting'.format(args.idx))
        node.sync_all()
        print('+ node {} is done waiting'.format(args.idx))
    else:
        print('- node {} is working'.format(args.idx))
        time.sleep(0.1)
