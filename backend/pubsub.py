from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import json_to_block
from backend.wallet.transaction import json_to_tx


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-06031688-9d29-11ea-84ed-1e1b4c21df71'
pnconfig.publish_key = 'pub-c-81c5f955-8b39-45ec-9f3c-dd2ca7ea21fb'



class Listener(SubscribeCallback):
    def __init__(self, blockchain, tx_pool):
        self.blockchain = blockchain
        self.tx_pool = tx_pool


    def message(self, pubnub, msg_object):
        print(f'\n-- Channel: {msg_object.channel} | Msg: {msg_object.message}')

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