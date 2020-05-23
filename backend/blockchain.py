from backend.block import Block, mine, check_block

GEN_BLOCK = Block(0, 'gen_prev_hash', 'gen_hash', ['gen_data'], 3, 'gen_nonce')


def check_chain(chain):
    # check incoming chain, block for block.
    if chain[0].__dict__ != GEN_BLOCK.__dict__:
        raise Exception('Incorrect Genesis Block!')

    for i in range(1, len(chain)):
        check_block(chain[i-1], chain[i], i)


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


if __name__ == "__main__":
    foochain =  Blockchain()
    newchain = Blockchain()

    for i in range(10):
        foochain.add(i)
        newchain.add(i)
        print(f'Block {i} found.')
    newchain.add(10)
    newchain.chain[5].prev_hash = 'bad_hash'

    foochain.replace(newchain.chain)

    print(foochain)