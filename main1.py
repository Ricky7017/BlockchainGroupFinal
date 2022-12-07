import json
import hashlib
from operator import itemgetter

from flask import Flask, render_template
from time import time
from uuid import uuid4


class Blockchain(object):
    difficulty_level = "0000"

    def __init__(self):
        self.chain = []
        self.current_transaction = []
        genesis_Hash = self.Block_Hash("genesis_block")
        self.append_block(
            Previous_block_hash=genesis_Hash,
            nonce=self.PoW(0, genesis_Hash, [])
        )

    # Hash the block
    def Block_Hash(self, block):
        # json.dumps covert the Python Object into JSON String
        blockEncoder = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockEncoder).hexdigest()

    # Proof of Work
    def PoW(self, index, Previous_block_hash, transactions):
        nonce = 0
        time1 = time()
        while self.validate_proof(index, Previous_block_hash,
                                  transactions, nonce) is False:
            nonce += 1
            print(nonce)
        time_total = time() - time1
        print(time_total)
        print(nonce)
        return nonce

    # Makes sure the PoW is correct
    def validate_proof(self, index, Previous_block_hash, transactions, nonce):
        data = f'{index},{Previous_block_hash},{transactions},{nonce}'.encode()
        hash_data = hashlib.sha256(data).hexdigest()
        return hash_data[:len(self.difficulty_level)] == self.difficulty_level

    # add the block to the chain
    def append_block(self, nonce, Previous_block_hash):
        block = {
            'index': len(self.chain),
            'transactions': self.current_transaction,
            'timestamp': time(),
            'nonce': nonce,
            'Previous_block_hash': Previous_block_hash
        }
        self.current_transaction = []
        self.chain.append(block)
        return block

    # add the vote to the block
    def add_vote(self, election, voter_ID, candidate_vote):
        self.current_transaction.append({
            'candidate_vote': candidate_vote,
            'voter_ID': voter_ID,
            'election': election
        })
        return self.last_block['index'] + 1

    # return the last block in the block chain
    @property
    def last_block(self):
        return self.chain[-1]