import time

from backend.blockchain.hashing import hashing
from backend.config import MINING_RATE


def mine(prev_block, data):
    nonce = 0
    timestamp = time.time_ns()
    diff = adj_diff(prev_block, timestamp)
    hash = hashing(timestamp, prev_block.hash, data, diff, nonce)


    while hash[0:diff] != '0' * diff:
        nonce += 1
        timestamp = time.time_ns()
        diff = adj_diff(prev_block, timestamp)
        hash = hashing(timestamp, prev_block.hash, data, diff, nonce)

    return Block(timestamp, prev_block.hash, hash, data, diff, nonce)
        


def adj_diff(prev_block, timestamp):
    if (timestamp - prev_block.timestamp) < MINING_RATE:
        return prev_block.difficulty + 1

    if (prev_block.difficulty - 1) > 0:
        return prev_block.difficulty - 1

    return 1


def check_block(prev_block, block, index=None):
    # ensure that: correct hash, diff adj only 1, correct last hash, proof of work
    if block.prev_hash != prev_block.hash:
        raise Exception(f'prev_hash incorrect @ Block {index}!')

    if block.hash[0:block.difficulty] != '0' * block.difficulty:
        raise Exception(f'POW incorrect @ Block {index}!')

    if abs(prev_block.difficulty - block.difficulty) > 1:
        raise Exception(f'diff adj more than 1 @ Block {index}!')

    check_hash = hashing(block.timestamp, block.prev_hash, block.data, block.difficulty, block.nonce)
    
    if block.hash != check_hash:
        raise Exception(f'hash incorrect @ Block {index}!')


def json_to_block(json):
    return Block(**json)


class Block:
    def __init__(self, timestamp, prev_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return f'Block: timestamp: {self.timestamp}, prev_hash: {self.prev_hash}, hash: {self.hash}, data: {self.data}, diff: {self.difficulty}, nonce: {self.nonce}'
