import json
from web3 import Web3
from solcx import compile_standard, install_solc
from flask import jsonify
import requests


def compile(pathToContract):
    with open(pathToContract, "r") as file:
        delivery_file = file.read()
    install_solc('0.8.0')
    file_name = pathToContract.split("/")[1]
    compiled_delivery_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {file_name: {"content": delivery_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_delivery_sol, file)
    # get bytecode
    bytecode = compiled_delivery_sol["contracts"][file_name][file_name.split(".")[0]]["evm"]["bytecode"]["object"]
    # get abi
    abi = json.loads(compiled_delivery_sol["contracts"][file_name][file_name.split(".")[0]]["metadata"])["output"]["abi"]
    return bytecode, abi


def deploy_contract(bytecode, abi):
    
    # For connecting to ganache
    
    adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
    session = requests.Session()
    session.mount('http://', adapter)
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545', session=session))
    chain_id = 1337
        
    address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
    private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d" # leaving the private key like this is very insecure if you are working on real world project
    # # Create the contract in Python
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the number of latest transaction
    nonce = w3.eth.get_transaction_count(address)
    
    # build transaction
    transaction = contract.constructor(address).transact(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction)
    contract_address = transaction_receipt.contractAddress
    print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")
    return contract_address, abi


