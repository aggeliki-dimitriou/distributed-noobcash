from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import json


class Transaction:

    def __init__(self, sender_address, recipient_address, amount, transaction_inputs, transaction_id = None, transaction_outputs = [], signature = None):
        self.sender_address = sender_address 
        self.recipient_address = recipient_address 
        self.amount = amount
        self.transaction_id = transaction_id
        self.transaction_inputs = transaction_inputs
        self.transaction_outputs = transaction_outputs
        self.signature = signature

    

    def to_json(self):
        trans_dict = self.__dict__
        if trans_dict['signature'] != None:
                trans_dict['signature'] = trans_dict['signature'].decode("utf-8") if type(trans_dict['signature']) == bytes else trans_dict['signature']
        return json.dumps(trans_dict)

    def create_transaction_id(self):
         self.transaction_id = str(SHA256.new(self.to_json().encode()).hexdigest())

    def sign_transaction(self, priv_key):
        """
        Sign transaction with private key
        """
        object_hash = SHA256.new(data = self.transaction_id.encode())
        signer = PKCS1_v1_5.new(priv_key)
        self.signature = base64.b64encode(signer.sign(object_hash))
       
    def verify_signature(self):
        pub_rsa = RSA.importKey(self.sender_address.encode())
        verifier = PKCS1_v1_5.new(pub_rsa)
        objest_hash = SHA256.new(data = self.transaction_id.encode())
        return verifier.verify(objest_hash, base64.b64decode(self.signature))
