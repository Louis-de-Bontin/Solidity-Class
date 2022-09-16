from solcx import compile_standard, install_solc
import json
from web3 import Web3
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv('../../env/.env')

# Launch Ganache : `./ganache-2.5.4-linux-x86_64.AppImage`

# Read sol
with open('./SimpleStorage.sol', 'r') as f:
    simple_storage_file = f.read()
    # print(simple_storage_file)

# Compile sol
install_solc("0.7.0"),
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                },
            },
        },
    },
    solc_version="0.7.0",
)

# Dump the compiled contract into a file
with open('compiled_solidity.json', 'w') as f:
    json.dump(compiled_sol, f, indent=4)

# Get objects from compiled_sol
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# Connect to local Ganache
w3 = Web3(Web3.HTTPProvider(
    "https://rinkeby.infura.io/v3/cfae6b4395d14c3b9a6f320b576542c9"))
chain_id = 4
my_address = os.environ.get('ADDRESS')
my_private_key = os.environ.get('PRIVATE_KEY')

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
print(f'Nonce : {nonce}')

print('deploying contract...')
tx = SimpleStorage.constructor().build_transaction(
    {'chainId': chain_id, "gasPrice": w3.eth.gas_price,
        'from': my_address, 'nonce': nonce}
)
signed_tx = w3.eth.account.sign_transaction(tx, my_private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('deployed!')
simple_storage_contract = w3.eth.contract(
    abi=abi, address=tx_receipt.contractAddress)

print('calling contract')
# Interact with the contract without making TXs (doesn't change the blockchain status)
call = simple_storage_contract.functions.store(666).call()
retrieve = simple_storage_contract.functions.retrieve().call()
print(f'Call : {call}')
print(f'Retrieve call: {retrieve}')

print('sending transaction')
# Interact with the contract by making TXs (changes the blockchain status)
call = simple_storage_contract.functions.store(666).build_transaction(
    {'chainId': chain_id, 'from': my_address,
        'nonce': nonce + 1, "gasPrice": w3.eth.gas_price}
)  # Creates TX
signed_call = w3.eth.account.sign_transaction(call, my_private_key)  # Sign TX
tx_hash = w3.eth.send_raw_transaction(signed_call.rawTransaction)  # Send TX
tx_receipt = w3.eth.wait_for_transaction_receipt(
    tx_hash)  # Wait for TX execution
print(f'Retrieve TX : {simple_storage_contract.functions.retrieve().call()}')
