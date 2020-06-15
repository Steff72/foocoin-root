import uuid
import time

from backend.config import TX_ID_LENGHT, MINING_REWARD

from backend.wallet.wallet import verify


def time_ns():
    return int(time.time()*1000000000)


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
