from web3 import Web3
import solcx

# connect to the Ganache blockchain
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# check if the connection is successful
print(f"Connected to the local Ethereum (Ganche) network: {web3.is_connected()}")

# get the first account
account = web3.eth.accounts[0]
# print(account)

# check the balance
balance = web3.eth.get_balance(account)
print(f"Balance of account 0: {web3.from_wei(balance, 'ether')} Ether")

# send a transaction from one account to another
tx_hash = web3.eth.send_transaction({
    'from': web3.eth.accounts[0],
    'to': web3.eth.accounts[1],
    'value': web3.to_wei(1, 'ether')
})

# wait for the transaction to be mined
f_hash = web3.eth.wait_for_transaction_receipt(tx_hash)
print(F"Transaction completed! The final hash is {f_hash}")

balance = web3.eth.get_balance(account)
print(f"Balance of account 0: {web3.from_wei(balance, 'ether')} Ether")

# basic Solidity contract
contract_source_code = '''
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint public storedData;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint) {
        return storedData;
    }
}
'''

# if needed, you may need to install solcx
solcx.install_solc()

# compile the contract
compiled_sol = solcx.compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:SimpleStorage']

# deploy the contract
SimpleStorage = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = SimpleStorage.constructor().transact({'from': account})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# get the contract instance
contract_address = tx_receipt.contractAddress
simple_storage = web3.eth.contract(address=contract_address, abi=contract_interface['abi'])

# interact with the contract
simple_storage.functions.set(15).transact({'from': account})
stored_data = simple_storage.functions.get().call()
print(f"Stored data in contract: {stored_data}")

