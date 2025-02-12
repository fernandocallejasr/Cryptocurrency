import json
import uuid

from backend.config import STARTING_BALANCE
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
	encode_dss_signature,
	decode_dss_signature
) 
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class Wallet:
	"""An individual wallet for a miner.
	   Keeps track of the miner's balance.
	   Allows the miner to authorize transactions

	   Parameters:
	   				address: String. Unique string for each wallet's instance generated using uuid (Universally Unique Identifier)
	   				balance: Float. The wallet's balance.
	   				private key: ec (elliptic cryptography) generated object. Being generated from an ellipse you cannot
	   							 get the value of the private key knowing the public key
	   				public key: ec generated object. Generated from a random point selected in the ellipse from the private key
	"""

	def __init__(self, blockchain = None):
		self.blockchain = blockchain
		self.address = str(uuid.uuid4())[:8]
		self.private_key = ec.generate_private_key(
				ec.SECP256K1(),                     # The specific cryptography standard
				default_backend()
			)
		self.public_key = self.private_key.public_key()
		self.serialize_public_key()

	@property
	def balance(self):
		return Wallet.calculate_balance(self.blockchain, self.address)
	

	def sign(self, data):
		"""Generates a signature based on the data using the local private key.
		   The private key object contains a method.
		   Inputs:
		   			data: The data to be signed in the transaction.
		"""
		return decode_dss_signature( self.private_key.sign(
			json.dumps(data).encode('utf-8'), #Encoding with utf8 transform the code in a byte representation, but is only available for strings, json.dumps stringifies any type of data
			ec.ECDSA(hashes.SHA256())         
		) 
		)

	def serialize_public_key(self):
		"""
		Reset the public key to its serialized version
		"""
		self.public_key = self.public_key.public_bytes(
				encoding = serialization.Encoding.PEM,                     #PEM is a common encoding in the field of security
				format = serialization.PublicFormat.SubjectPublicKeyInfo   #Default option for the public bytes algorithm
			).decode('utf-8')

	@staticmethod
	def verify(public_key, data, signature):
		"""Verify a signature on the original public key and data.
		   When it gets an invalid signature throws an exception
		   Inputs: 
		   			public_key: Wallet's public key object.
		   			data: Unencoded version of the data used to create the signature.
		"""
		deserialized_public_key = serialization.load_pem_public_key(
			public_key.encode('utf-8'),
			default_backend()
		)

		(r, s) = signature

		try:
			deserialized_public_key.verify(
				encode_dss_signature(r,s), 
				json.dumps(data).encode('utf-8'),
				ec.ECDSA(hashes.SHA256())         #ECDSA digital signature algorithm specification used to create the signature.
			)
			return True
		except InvalidSignature:
			return False

	@staticmethod
	def calculate_balance(blockchain, address):
		"""
		Calculate the balance of the given address considering the transaction
		data within the blockchain
		"""
		balance = STARTING_BALANCE

		if not blockchain:
			return balance

		for block in blockchain.chain:
			for transaction in block.data:
				if transaction['input']['address'] == address:
					"""
					Any time the address conducts a new transaction it
					resets its balance
					"""
					balance = transaction['output'][address]
				elif address in transaction['output']:
					balance += transaction['output'][address]

		return balance



def main():
	wallet = Wallet()
	print(f'wallet.__dict__: {wallet.__dict__}')

	data = {'foo': 'bar'}
	signature = wallet.sign(data)
	print(f'signature: {signature}')

	should_be_valid = Wallet.verify(wallet.public_key, data, signature)
	print(f'should_be_valid: {should_be_valid}')

	should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
	print(f'should_be_invalid: {should_be_invalid}')

if __name__ == '__main__':
	main()