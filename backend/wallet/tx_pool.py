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
                print(tx)
                try: 
                    del self.tx_map[tx['id']]
                except KeyError:
                    pass