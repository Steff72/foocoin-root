import os
import random
import requests

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import time
import hashlib
import json
import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-06031688-9d29-11ea-84ed-1e1b4c21df71'
pnconfig.publish_key = 'pub-c-81c5f955-8b39-45ec-9f3c-dd2ca7ea21fb'


# mining rate in nanoseconds. => 5 seconds
MINING_RATE = 5000000000

# mining reward
MINING_REWARD = 10

# initial balance of wallet
INIT_BALANCE = 100

# lenght of wallet address
AD_LENGHT = 8

# lenght of transaction ID
TX_ID_LENGHT = 8



def hashing(*args):
    data = ''.join(sorted(map(lambda param: json.dumps(param), args)))

    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def time_ns():
    return int(time.time()*1000000000)


def mine(prev_block, data):
    nonce = 0
    timestamp = time_ns()
    diff = adj_diff(prev_block, timestamp)
    hash = hashing(timestamp, prev_block.hash, data, diff, nonce)


    while hash[0:diff] != '0' * diff:
        nonce += 1
        timestamp = time_ns()
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



GEN_BLOCK = Block(1, 'gen_prev_hash', 'gen_hash', [], 3, 'gen_nonce')


def check_chain(chain):
    # check incoming chain, block for block, and all transactions.
    if chain[0].__dict__ != GEN_BLOCK.__dict__:
        raise Exception('Incorrect Genesis Block!')

    for i in range(1, len(chain)):
        check_block(chain[i-1], chain[i], i)

    check_tx_chain(chain)


def check_tx_chain(chain):
    # ensure each tx exists only once, only one mining reward, each tx valid.
    # check input amounts of each tx according addresse's balance up to this point in time.
    tx_ids = set()

    for i in range(1, len(chain)):
        # start at 1 to except the gen block
        block = chain[i]

        reward_tx = False

        for tx_json in block.data:
            tx = json_to_tx(tx_json)

            if tx.id in tx_ids:
                raise Exception(f'Tx {tx.id} not unique!')
            tx_ids.add(tx.id)

            if tx.input == { 'address': 'MINING REWARD TRANSACTION' }:
                if reward_tx:
                    raise Exception('Multiple mining rewards in block {i}')
                reward_tx = True

            else:
                help_blockchain = Blockchain()
                help_blockchain.chain = chain[0:i]
                help_balance = cal_bal(help_blockchain, tx.input['address'])
                if help_balance != tx.input['amount']:
                    raise Exception(f'Tx {tx.id} has invalid input amount!')

            check_tx(tx)            


def json_to_blockchain(json_chain):
    blockchain = Blockchain()
    blockchain.chain = []

    for json_block in json_chain:
        blockchain.chain.append(json_to_block(json_block))

    return blockchain
    

class Blockchain:
    def __init__(self):
        # init with genesis Block.
        self.chain = [GEN_BLOCK]


    def add(self, data):
        # add Block with mine function using prev-hash and data.
        self.chain.append(mine(self.chain[-1], data))


    def replace(self, chain):
        # replace with incomming chain if correct and longer.
        if len(chain) <= len(self.chain):
            raise Exception('Incoming chain too short!')

        try:
            check_chain(chain)
        except Exception as e:
            raise Exception(f'Bad incomming chain: {e}!')
        
        # both check passed, replace local chain.
        self.chain = chain
        print('Chain replaced.')


    def __str__(self):
        return f'FooChain: {self.chain}'


    def json(self):
        json_chain = []

        for block in self.chain:
            json_chain.append(block.__dict__)

        return json_chain


def gen_id():
    return str(uuid.uuid4())[0:TX_ID_LENGHT]


def check_tx(tx):
    # check if valid mining reward
    if tx.input['address'] == 'MINING REWARD TRANSACTION':
        if list(tx.output.values()) != [MINING_REWARD]:
            raise Exception('Invalid mining reward!')
        return

    # check input = total of outputs
    output_total = sum(tx.output.values())
    if tx.input['amount'] != output_total:
        raise Exception('Invalid tx output values!')

    # check signature
    if not verify(tx.input['public_key'], tx.output, tx.input['signature']):
        raise Exception('Invalid signature!')


def json_to_tx(tx_json):
    # json from PubSub into Transaction instance
    return Transaction(**tx_json)


def reward_tx(miner_wallet):
    # reward tx for miner finding new block
    input = { 'address': 'MINING REWARD TRANSACTION' }
    output = {}
    output[miner_wallet.address] = MINING_REWARD

    return Transaction(output=output, input=input)


class Transaction:
    def __init__(
        self, 
        sender_wallet=None, 
        recipient=None, 
        amount=None, 
        id=None, 
        output=None, 
        input=None
    ):
        self.id = id or gen_id()
        self.output = output or self.gen_output(sender_wallet, recipient, amount)
        self.input = input or {
            'timestamp': time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(self.output)
        }


    def gen_output(self, sender_wallet, recipient, amount):
        #data for output of TX

        if amount > sender_wallet.balance:
            raise Exception('Sender Balance too low!')

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output


    def update(self, sender_wallet, recipient, amount):

        if amount > self.output[sender_wallet.address]:
            raise Exception('Sender Balance too low!')

        if recipient in self.output:
            self.output[recipient] += amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] -= amount

        self.input = {
            'timestamp': time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(self.output)
        }


class TxPool:
    def __init__(self):
        self.tx_map = {}


    def set_tx(self, tx):
        self.tx_map[tx.id] = tx


    def existing_tx(self, address):
        for tx in self.tx_map.values():
            if tx.input['address'] == address:
                return tx


    def tx_data(self):
        # tx from pool in json format
        tx_values = self.tx_map.values()
        tx_data = list(map(lambda tx: tx.__dict__, tx_values))

        return tx_data


    def clear_blockchain_tx(self, blockchain):
        # remove tx in blockchain from tx_pool
        for block in blockchain.chain:
            for tx in block.data:
                try: 
                    del self.tx_map[tx['id']]
                except KeyError:
                    pass



def gen_address():
    return str(uuid.uuid4())[0:AD_LENGHT]

def gen_priv_key():
    return ec.generate_private_key(ec.SECP256K1(), default_backend())

def encode_data(data):
    return json.dumps(data).encode('utf-8')


def verify(public_key, data, signature):
    # verify the signature of a transaction
    deserialized_public_key = serialization.load_pem_public_key(
        public_key.encode('utf-8'),
        default_backend()
    )

    (r, s) = signature

    try:
        # pylint: disable=all
        deserialized_public_key.verify(
            encode_dss_signature(r, s), encode_data(data), ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False


def cal_bal(blockchain, address):
    # calculating the balance of address by searching the blockchain
    # if tx from address >> reset balance to remainder
    # if address in output of tx >> add to the balance

    balance = INIT_BALANCE

    if not blockchain:
        return balance

    for block in blockchain.chain:
        for tx in block.data:
            if tx['input']['address'] == address:
                balance = tx['output'][address]
            elif address in tx['output']:
                balance += tx['output'][address]

    return balance



class Wallet:
    def __init__(self, blockchain=None):
        self.address = gen_address()
        self.private_key = gen_priv_key()
        self.public_key = self.private_key.public_key()
        self.blockchain = blockchain
        self.serialize_public_key()

    @property
    def balance(self):
        return cal_bal(self.blockchain, self.address)


    def sign(self, data):
        byte_data = encode_data(data)

        return decode_dss_signature(self.private_key.sign(byte_data, ec.ECDSA(hashes.SHA256())))


    def serialize_public_key(self):
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')



class Listener(SubscribeCallback):
    def __init__(self, blockchain, tx_pool):
        self.blockchain = blockchain
        self.tx_pool = tx_pool


    def message(self, pubnub, msg_object):
        print(f'\n-- Channel: {msg_object.channel} | {msg_object.message}')

        if msg_object.channel == 'BLOCK':
            block = json_to_block(msg_object.message)
            maybe_chain = self.blockchain.chain[:]
            maybe_chain.append(block)

            try:
                self.blockchain.replace(maybe_chain)
                self.tx_pool.clear_blockchain_tx(self.blockchain)
                print('\n -- Local chain replaced.')
            except Exception as e:
                print(f'\n -- {e}')

        elif msg_object.channel == 'TX':
            tx = json_to_tx(msg_object.message)
            self.tx_pool.set_tx(tx)
            print('\n -- Incoming Tx sent to TxPool.')


class PubSub():
    # establish communication between nodes
    def __init__(self, blockchain, tx_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(['BLOCK', 'TX']).execute()
        self.pubnub.add_listener(Listener(blockchain, tx_pool))


    def publish(self, channel, msg):
        self.pubnub.publish().channel(channel).message(msg).sync()


    def publish_block(self, block):
        # publish new block to nodes
        self.publish('BLOCK', block.__dict__)


    def publish_tx(self, tx):
        # publish new transaction to nodes
        self.publish('TX', tx.__dict__)







app = Flask(__name__)
 # Cross-origin resource sharing setup
CORS(app, resources={ r'/*': { 'origins': '*' } })
# avoid sorting of output and input transaction
app.config['JSON_SORT_KEYS'] = False

foochain = Blockchain()
wallet = Wallet(foochain)
tx_pool = TxPool()
pubsub = PubSub(foochain, tx_pool)


@app.route('/')
def default():
    return render_template('index.html')


@app.route('/api/blockchain')
def blockchain():
    return jsonify(foochain.json())


@app.route('/api/blockchain/page')
def page():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    return jsonify(foochain.json()[::-1][start:end])


@app.route('/api/blockchain/length')
def length():
    return jsonify(len(foochain.chain))


@app.route('/api/blockchain/mine', methods=['POST'])
def mine_route():
    tx_data = tx_pool.tx_data()
    tx_data.append(reward_tx(wallet).__dict__)
    foochain.add(tx_data)
    block = foochain.chain[-1]
    pubsub.publish_block(block)
    tx_pool.clear_blockchain_tx(foochain)

    return jsonify(block.__dict__)


@app.route('/api/wallet/transact', methods=['POST'])
def transact():
    tx_data = request.get_json()
    tx = tx_pool.existing_tx(wallet.address)

    if tx:
        tx.update(wallet, tx_data['recipient'], tx_data['amount'])
    else:
        tx = Transaction(wallet, tx_data['recipient'], tx_data['amount'])
    
    pubsub.publish_tx(tx)

    return jsonify(tx.__dict__)


@app.route('/api/wallet/info')
def info():
    return jsonify({ 'address': wallet.address, 'balance': wallet.balance })


@app.route('/api/known-addresses')
def known_addresses():
    known_addresses = set()

    for block in foochain.chain:
        for tx in block.data:
            outputAdresses = tx['output'].keys()

            if wallet.address in outputAdresses:
                known_addresses.update(outputAdresses)

        known_addresses.discard(wallet.address)

    return jsonify(list(known_addresses))


@app.route('/api/transactions')
def transactions():
    return jsonify(tx_pool.tx_data())



# PORT = 5000

# if os.environ.get('PEER') == 'True':
#     PORT = random.randint(5001, 6000)

#     # synchronize blockchain at startup for PEERS
#     response = requests.get('http://localhost:5000/api/blockchain')
#     blockchain = json_to_blockchain(response.json())

#     try:
#         foochain.replace(blockchain.chain)
#         print('\n -- Local chain updated.')
#     except Exception as e:
#         print(f'\n -- Chain sync error: {e}')

# if os.environ.get('SEED') == 'True':
for i in range(10):
    foochain.add([
        Transaction(Wallet(), Wallet().address, random.randint(2, 50)).__dict__,
        Transaction(Wallet(), Wallet().address, random.randint(2, 50)).__dict__
    ])

for i in range(3):
    tx_pool.set_tx(Transaction(Wallet(), Wallet().address, random.randint(2,50)))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

