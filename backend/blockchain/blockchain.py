from backend.blockchain.block import Block, mine, check_block, json_to_block
from backend.wallet.transaction import json_to_tx, check_tx
from backend.wallet.wallet import cal_bal

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


