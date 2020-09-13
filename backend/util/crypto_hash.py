import hashlib
import json

def crypto_hash(*args):
	"""Returns a SHA-256 hash of the given data.
	"""
	# Una forma de convertir todo tipo de data en strings es con el método json.dumps()
	# Necesario ya que sólo los strings tienen acceso al método .encode() usado abajo
	stringified_args = sorted(map(lambda data: json.dumps(data), args))
	joined_data = ''.join(stringified_args)

	#aplicamos el método .encode() a data porque Unicode-objects must be encoded before hashing
	#y el método .hexdigest() para mostrar representación del objeto sha-256
	return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
	print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
	print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
	main()