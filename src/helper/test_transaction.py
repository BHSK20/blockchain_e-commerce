from web3 import Web3
from hexbytes import HexBytes
INFURA_API_KEY = '7896f3612eca4491bb7a895198929bac'
# Khởi tạo đối tượng Web3
web3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{INFURA_API_KEY}'))
contract_address = '0x7819188be76a23C04Fa416C6B6708a80418b5f9b'
# ABI
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_transactionId",
				"type": "uint256"
			}
		],
		"name": "confirmTransaction",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_transactionId",
				"type": "uint256"
			}
		],
		"name": "executeTransaction",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_tokenContract",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "submitTransaction",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address[]",
				"name": "_owners",
				"type": "address[]"
			},
			{
				"internalType": "uint256",
				"name": "_numConfirmationsRequired",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "transactionId",
				"type": "uint256"
			}
		],
		"name": "TransactionConfirmed",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "transactionId",
				"type": "uint256"
			}
		],
		"name": "TransactionExecuted",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "transactionId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "tokenContract",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "TransactionSubmitted",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "getTransactionsLength",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "numConfirmationsRequired",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "owners",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "transactions",
		"outputs": [
			{
				"internalType": "address",
				"name": "tokenContract",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "executed",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

if web3.is_address(contract.address):
    print("Contract address deposit is valid")
else:
    print("Contract address deposit is not valid")
ad_address = '0xa93976cFB34A7aEDA88fa67fDE8f355C0ada3b7B'
def check(from_address: str, private_key: str, amount: int, to_address: str):
    nonce = web3.eth.get_transaction_count(from_address, 'latest')
    print(nonce)
    block_number = web3.eth.get_block('latest')
    print(block_number)
    # approve
    build_dict = {'from': from_address, 'nonce': nonce, 'gas': 4000000, 'gasPrice': web3.to_wei('50', 'gwei')}
    transfer_data = contract.functions.transfer(to_address, web3.to_wei(amount, 'ether')).build_transaction(build_dict)
    signed_txn = web3.eth.account.sign_transaction(transfer_data, private_key=private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print('transaction_hash: ', transaction_hash.hex())
    # confirm
    return transaction_hash
def status_value_of_transaction(tx_hash):
    res = web3.eth.get_transaction_receipt(tx_hash)
    logs = contract.events.Transfer().process_receipt(res)
    print(logs)
    # Using the get method
    value = logs[0].args.get('value')
    value_in_ether = web3.from_wei(value, 'ether')
    status = res['status']
    return status, value_in_ether
