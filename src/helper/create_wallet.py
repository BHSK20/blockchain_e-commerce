from web3 import Web3
from src.config import config
from eth_account import Account
INFURA_API_KEY = config.INFURA_API_KEY
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/{}'.format(INFURA_API_KEY)))

def create_wallet():
    # Generate a new Ethereum account
    account = Account.create()
    # Get the address and private key
    address = account.address
    private_key = account.privateKey.hex()
    return address, private_key
