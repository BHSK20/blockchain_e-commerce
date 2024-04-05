from web3 import Web3
from hexbytes import HexBytes
INFURA_API_KEY = '7896f3612eca4491bb7a895198929bac'
# Khởi tạo đối tượng Web3
web3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{INFURA_API_KEY}'))
contract_address = '0x7819188be76a23C04Fa416C6B6708a80418b5f9b'
# ABI
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
# Check if the contract address is valid
is_valid_address = web3.is_address(contract.address)

if is_valid_address:
    print("Contract address is valid")
else:
    print("Contract address is not valid")

def getBalance(address):
    return contract.functions.balanceOf(address).call()
def get_balance_in_ether(address):
    value = contract.functions.balanceOf(address).call()
    return float(web3.from_wei(value, 'ether'))
def checkBalance(address, amount):
    return getBalance(address) >= web3.to_wei(amount, 'ether')
def transfer(from_address: str, private_key: str, amount: int, to_address: str):
    nonce = web3.eth.get_transaction_count(from_address, 'latest')
    print(nonce)
    build_dict = {'from': from_address, 'nonce': nonce, 'gas': 4000000, 'gasPrice': web3.to_wei('50', 'gwei')}
    transfer_data = contract.functions.transfer(to_address, web3.to_wei(amount, 'ether')).build_transaction(build_dict)
    signed_txn = web3.eth.account.sign_transaction(transfer_data, private_key=private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print('transaction_hash: ', transaction_hash.hex())
    return transaction_hash

def wait_for_transaction(tx_hash):
    transaction_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=500)
    return tx_hash, transaction_receipt

def transaction_info(tx_hash):
    return web3.eth.get_transaction(tx_hash)

def convert_hexbytes_to_string(obj):
    if isinstance(obj, dict):
        return {k: convert_hexbytes_to_string(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_hexbytes_to_string(item) for item in obj]
    elif isinstance(obj, HexBytes):
        return obj.hex()
    else:
        return obj

def status_value_of_transaction(tx_hash):
    res = web3.eth.get_transaction_receipt(tx_hash)
    logs = contract.events.Transfer().process_receipt(res)
    print(logs)
    # Using the get method
    value = logs[0].args.get('value')
    value_in_ether = web3.from_wei(value, 'ether')
    status = res['status']
    return status, value_in_ether
