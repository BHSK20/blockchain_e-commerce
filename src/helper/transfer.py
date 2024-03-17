from web3 import Web3, Account
from web3.middleware import geth_poa_middleware
from src.config import config
from web3 import Web3, Account
from web3.middleware import geth_poa_middleware
from src.config import config
from src.config import config
import json

def transfer(from_address: str, private_key: str, amount: int, to_address: str):
    # Connect to Sepolia testnet
    INFURA_API_KEY = config.INFURA_API_KEY
    web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/{}'.format(INFURA_API_KEY)))
    if web3.is_connected():
        print("Connection successful")
    else:
        print("Connection failed")
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Get the balance of the from_address
    balance = web3.eth.get_balance(from_address, block_identifier='latest')
    if balance < web3.to_wei(amount, 'ether'):
        print("Insufficient balance")
        return

    # Get the nonce
    nonce = web3.eth.get_transaction_count(from_address)

    # Prepare the transaction
    transaction = {
        'to': to_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 20000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
        'chainId': config.CHAIN_ID
    }

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    transaction_json = json.dumps(dict(transaction), default=str)
    return web3.to_hex(txn_hash), transaction_json
