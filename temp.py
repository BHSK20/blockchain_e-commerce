from web3 import Web3
from src.config import config
INFURA_API_KEY = config.INFURA_API_KEY
# Khởi tạo đối tượng Web3
web3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{INFURA_API_KEY}'))
def get_ether_balance(address):
    balance = web3.eth.get_balance(address)
    ether_balance = web3.from_wei(balance, 'ether')
    return ether_balance

print(get_ether_balance(config.AD_PUBLIC_KEY))