import json
import web3 

from web3 import Web3
from solc import compile_files, link_code, compile_source

# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
def deploy_contract(contract_interface):
 w3.eth.defaultAccount = w3.eth.accounts[1] 
 # Instantiate and deploy contract
 contract = w3.eth.contract(
 abi=contract_interface['abi'],
 bytecode=contract_interface['bin']
 )
 print("tttttttttttttt :",w3.eth.accounts)
 # Get transaction hash from deployed contract
 #tx_hash =contract.functions.deploy(transaction={'from':w3.eth.accounts[1]})
 tx_hash = contract.constructor().transact() 
 # Get tx receipt to get contract address
 tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
 print("tx_receipt :",tx_receipt)
 return tx_receipt['contractAddress']# compile all contract files
contracts = compile_files(['user.sol', 'stringUtils.sol'])# separate main file and link file
main_contract = contracts.pop("user.sol:userRecords")


library_link = contracts.pop("stringUtils.sol:StringUtils")

# print bin part in console you will see 'stringUtils' in that we need to link library address in that bin code.
# to that we have to deploy library code first then link it
dep=deploy_contract(library_link)
library_address = {
 "stringUtils.sol:StringUtils": dep
}
main_contract['bin'] = link_code(
 main_contract['bin'], library_address)


contract_address = deploy_contract(main_contract)
print(contract_address)
# add abi(application binary interface) and transaction reciept in json file
with open('data.json', 'w') as outfile:
 data = {
 "abi": main_contract['abi'],
 "contract_address": contract_address
 }
 json.dump(data, outfile, indent=4, sort_keys=True)
