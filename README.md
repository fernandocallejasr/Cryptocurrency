# Blockchain application

This project is a blockchain application in which you can conduct transactions using your wallet, every transaction is stored in the transaction pool.

![Image 1](/images/frontend-sc-1.png)
![Image 2](/images/frontend-sc-2.png)


The transaction pool that contains multiple transactions, can be stored safely and publicly in blocks, delivered to every peer in the blockchain network using the shared chain. 

The backend is written in python. To be part of the official blockchain, every block must conform to the rules of the blockchain technology, those are:

1. The last-hash property must equal the value of the hash property given in the prior block.
2. The given hash must be able to be generated given the information contained in the block, that means that every peer in the blockchain network can validate the authenticity of the chain. This creates a layer of security given that the change of a single character in the information stored, will create a completely different hash.
3. The start of the hash must contain the same number of "0" of the difficulty property in the block.
![Image 3](/images/frontend-sc-3.png)
The blockchain is generated when one peer mines a block, and to promote that activity, which requires a proof of work, that can be translated into computational work, the user receives some credit every time they are able to mine a block into the blockchain.

![Image 4](/images/frontend-sc-4.png)


# How to get started

**Create a virtual environment**
I named this virtual environment py3-blockchain because I used python 3, and you should use that version too, but you can change the name of the environment, I also created the environment using conda but you can create it in your terminal.
In this virtual environment, you will install all the packages mentioned in the requirements.txt file.

**Activate the virtual environment**
Inside the conda prompt
```
conda activate py3-blockchain
```

**Install all the packages**

```
pip install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment
```
python -m pytest backend/tests
```

**Seed the backend with data and run the application and API**

Make sure to activate the virtual environment.

```
set SEED_DATA=True
python -m backend.app
```

**Run the frontend**

In the frontend directory:
```
npm run start
```
