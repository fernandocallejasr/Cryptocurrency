import time
import uuid

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

class Transaction:
	"""Document of an exchange in currency from a sender to one 
	   or more recipients (Destinatario)

	   Parameters:
	   				sender_wallet: Instance of the Wallet class, accessing to its sign method allows us to generate a signature for the transaction.   class String. The sender's address.
	   				recipient (Beneficiario): String. The final destination's address
	   				amount: Float. How much currency is exchanged.

					input: Meta information about the transaction such as timestamp, sender's address, public key and signature.
	   				output: Data Structure. Records who the recipients are, and the amount of the transaction.
	"""
	def __init__(
		self, 
		sender_wallet = None, 
		recipient = None, 
		amount = None, 
		id = None, 
		output = None, 
		input = None
	):
		self.id = id or str(uuid.uuid4())[:8]       # Unique ID for each transaction, generated form uuid (Universally Unique Identificacion)
		self.output = output or self.create_output(
			sender_wallet,
			recipient,
			amount		
		)
		self.input = input or self.create_input(sender_wallet, self.output)
	
	def create_output(self, sender_wallet, recipient, amount):
		"""Structure the output data for the transaction

		   Inputs:
		   			recipient: String. The beneficiary's wallet's address

		   	Outputs:
		   			recipient: key-value pair of the recipients address and the amount being recieved.
		   			sender's address: key-value pair of the sender's wallet address. It is made a recipient because the t
		   							  transaction must record how much currency the sender must have after the transaction is completed.
		   							  we can say is the change of the transaction.
		"""
		if amount > sender_wallet.balance:
			raise Exception('Amount excedes balance')

		output = {}
		output[recipient] = amount
		output[sender_wallet.address] = sender_wallet.balance - amount

		return output
	
	def create_input(self, sender_wallet, output):
		"""Structure the input data for the transaction
		   Signs the transaction and includes the sender's public key and address
		"""
		return {
			'timestamp': time.time_ns(), 
			'amount': sender_wallet.balance, 
			'address': sender_wallet.address,
			'public_key': sender_wallet.public_key,
			'signature': sender_wallet.sign(output)
		}

	def update(self, sender_wallet, recipient, amount):
		"""Updates the transaction with an existing or new recipient
		"""
		if amount > self.output[sender_wallet.address]:
			raise Exception('Amount exceeds balance')

		if recipient in self.output:
			self.output[recipient] += amount
		else:
			self.output[recipient] = amount

		self.output[sender_wallet.address] -= amount

		self.input = self.create_input(sender_wallet, self.output)

	def to_json(self):
		"""Serialize the transaction.
		"""
		return self.__dict__

	@staticmethod
	def from_json(transaction_json):
		"""
		Deserialize the transaction's json representation back into a
		Transaction instance
		"""
		return Transaction(**transaction_json)


	@staticmethod
	def is_valid_transaction(transaction):
		"""Validate a transaction.
		   Raise an exception for invalid transactions.
		"""
		if transaction.input == MINING_REWARD_INPUT:
			if list(transaction.output.values()) != [MINING_REWARD]:
				raise Exception('Invalid mining reward')
			return

		output_total = sum(transaction.output.values())	

		if transaction.input['amount'] != output_total:
			raise Exception('Invalid transaction output values')

		if not Wallet.verify(
			transaction.input['public_key'],
			transaction.output, 
			transaction.input['signature']
		):
	 		raise Exception('Invalid signature')

	@staticmethod
	def reward_transaction(miner_wallet):
		"""
		Generate a reward transaction that awards the mines
		"""
		output = {}
		output[miner_wallet.address] = MINING_REWARD

		return Transaction(input = MINING_REWARD_INPUT, output = output)

def main():
	transaction = Transaction(Wallet(), 'recipient', 15)
	print(f'transaction.__dict__: {transaction.__dict__}')

	transaction_json = transaction.to_json()
	restored_transaction = Transaction.from_json(transaction_json)
	print(f'restored_transaction.__dict__: {restored_transaction.__dict__}')

if __name__ == '__main__':
	main()



