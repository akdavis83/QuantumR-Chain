import hashlib
import json
import os
from time import time
from kyber import Kyber1024
import base58
from ecdsa import SigningKey, VerifyingKey, SECP256k1


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.balances = {}
        self.user_wallets = {}  # {user_id: {'password': hashed_password, 'keys': [{'public_key', 'private_key', 'address'}]}}
        self.create_genesis_block()

    def create_genesis_block(self):
        total_supply = 42_000_000
        genesis_address = "CUtqbuVuiAtwCXLUEpCMLyYKdXcxm98iY"
        self.balances[genesis_address] = total_supply
        self.chain.append({
            'index': 1,
            'timestamp': time(),
            'transactions': [
                {'sender': "0", 'recipient': genesis_address, 'amount': total_supply}
            ],
            'proof': 0,
            'previous_hash': '0',
        })

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount, signature):
        if sender != "0" and self.balances.get(sender, 0) < amount:
            raise ValueError("Insufficient balance")

        # Verify the transaction
        transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
        if not self.verify_signature(sender, transaction, signature):
            raise ValueError("Invalid signature")

        # Update balances
        if sender != "0":
            self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount

        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1

    def generate_keys(self, user_id, password=None):
        if user_id in self.user_wallets and not password:
            return {"error": "User ID already exists, use export_keys"}

        # Derive seed from user ID and password, or generate random seed
        if password:
            seed = hashlib.sha3_256(f"{user_id}{password}".encode()).digest()
        else:
            seed = os.urandom(32)

        # Generate Kyber1024 key pair
        pk, sk = Kyber1024.keygen()
        address = base58.b58encode_check(hashlib.sha3_256(pk).digest()[:20]).decode()

        # Initialize wallet if not already present
        if user_id not in self.user_wallets:
            self.user_wallets[user_id] = {'password': hashlib.sha3_256(password.encode()).hexdigest() if password else None, 'keys': []}

        # Store key pair and address
        key_entry = {'public_key': pk.hex(), 'private_key': sk.hex(), 'address': address}
        self.user_wallets[user_id]['keys'].append(key_entry)

        # Initialize balance for the new address
        self.balances[address] = 0
        return key_entry

    def sign_transaction(self, user_id, address, recipient, amount):
        if user_id not in self.user_wallets:
            raise ValueError("User ID not found")

        # Find the private key for the given address
        keys = self.user_wallets[user_id]['keys']
        private_key = None
        for key in keys:
            if key['address'] == address:
                private_key = key['private_key']
                break

        if not private_key:
            raise ValueError("Address not found")

        # Sign the transaction
        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        transaction = {'sender': address, 'recipient': recipient, 'amount': amount}
        message = json.dumps(transaction, sort_keys=True).encode()
        signature = sk.sign(message).hex()
        return signature
    
    def verify_signature(self, address, transaction, signature):
         if address == "0":
            return True

         for user_id, wallet_data in self.user_wallets.items():
             for key_data in wallet_data['keys']:
                 if key_data['address'] == address:
                     public_key = key_data['public_key']
                     try:
                         vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
                         message = json.dumps(transaction, sort_keys=True).encode()
                         vk.verify(bytes.fromhex(signature), message)
                         return True
                     except:
                        return False

         return False

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha3_256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha3_256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    def get_keys(self, user_id):
        if user_id not in self.user_wallets:
            return {"error": "User ID not found"}
        return self.user_wallets[user_id]

    def export_keys(self, user_id, address):
        if user_id not in self.user_wallets:
            return {"error": "User ID not found"}

        for key in self.user_wallets[user_id]['keys']:
            if key['address'] == address:
                return key

        return {"error": "Address not found"}

    def get_balance(self, address):
        return self.balances.get(address, 0)