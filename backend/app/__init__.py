import os
import random
import requests

from flask import Flask, jsonify, request

from backend.blockchain.blockchain import Blockchain, json_to_blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction, reward_tx
from backend.wallet.tx_pool import TxPool
from backend.pubsub import PubSub


app = Flask(__name__)
foochain = Blockchain()
wallet = Wallet(foochain)
tx_pool = TxPool()
pubsub = PubSub(foochain, tx_pool)


@app.route('/')
def default():
    return 'Welcome to Foochain'


@app.route('/blockchain')
def blockchain():
    return jsonify(foochain.json())


@app.route('/blockchain/mine', methods=['POST'])
def mine():
    tx_data = tx_pool.tx_data()
    tx_data.append(reward_tx(wallet).__dict__)
    foochain.add(tx_data)
    block = foochain.chain[-1]
    pubsub.publish_block(block)
    tx_pool.clear_blockchain_tx(foochain)

    return jsonify(block.__dict__)


@app.route('/wallet/transact', methods=['POST'])
def transact():
    tx_data = request.get_json()
    tx = tx_pool.existing_tx(wallet.address)

    if tx:
        tx.update(wallet, tx_data['recipient'], tx_data['amount'])
    else:
        tx = Transaction(wallet, tx_data['recipient'], tx_data['amount'])
    
    pubsub.publish_tx(tx)

    return jsonify(tx.__dict__)


@app.route('/wallet/info')
def info():
    return jsonify({ 'address': wallet.address, 'balance': wallet.balance })



PORT = 5000

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    # synchronize blockchain at startup for PEERS
    response = requests.get('http://localhost:5000/blockchain')
    blockchain = json_to_blockchain(response.json())

    try:
        foochain.replace(blockchain.chain)
        print('\n -- Local chain updated.')
    except Exception as e:
        print(f'\n -- Chain sync error: {e}')

app.run(port=PORT)