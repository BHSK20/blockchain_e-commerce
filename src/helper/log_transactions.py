from web3 import Web3, HTTPProvider

# Function to get the last checked block number
def get_last_checked_block():
    # Replace this with your actual code to get the last checked block number
    # For example, you could get it from a database or a file
    return 0

# Function to set the last checked block number
def set_last_checked_block(block_number):
    # Replace this with your actual code to set the last checked block number
    # For example, you could set it in a database or a file
    pass

def log_transaction_history(address):
    # Connect to the Ethereum network
    web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

    # Get the last checked block number
    last_checked_block = get_last_checked_block()

    # Get the latest block number
    latest_block = web3.eth.blockNumber

    # Loop through the blocks
    for block_number in range(last_checked_block + 1, latest_block + 1):
        block = web3.eth.getBlock(block_number, full_transactions=True)

        # Loop through the transactions in the block
        for transaction in block.transactions:
            # Check if the address is the sender or receiver of the transaction
            if transaction['from'] == address or transaction['to'] == address:
                print(f"Block: {block_number}, Transaction Hash: {transaction['hash'].hex()}, From: {transaction['from']}, To: {transaction['to']}, Value: {web3.fromWei(transaction['value'], 'ether')} Ether")

        # Set the last checked block number
        set_last_checked_block(block_number)