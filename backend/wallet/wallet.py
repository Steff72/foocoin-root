import uuid
import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

from backend.config import INIT_BALANCE, AD_LENGHT


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
