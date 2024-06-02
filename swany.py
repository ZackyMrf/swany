from web3 import Web3, HTTPProvider
from solcx import compile_standard, install_solc
import json
import time
import secrets
from eth_account import Account
install_solc('0.8.25')

with open("swany.sol", "r") as file:
    swan_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"swany.sol": {"content": swan_file}},
        "settings": {
             "evmVersion": "london",
             "optimizer": {
             "enabled": bool(True),
             "runs": 200
            },
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                }
            }
        },
    },
    solc_version="0.8.25",
)

bytecode = compiled_sol["contracts"]["swany.sol"]["MessageContract"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["swany.sol"]["MessageContract"]["metadata"])["output"]["abi"]

web3 = Web3(Web3.HTTPProvider("https://rpc-proxima.swanchain.io"))
chainId = int(20241133)

#connecting web3
if  web3.is_connected() == True:
    print("Web3 Connected...\n")
else :
    print("Error Connecting Please Try Again...")

#============================================================================
def MainCall(sender, senderkey):
    contractswan = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    #estimate gas limit contract
    gas_tx = contractswan.constructor().build_transaction({
        'chainId': chainId,
        'from': sender,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender)
    })
    gasAmount = web3.eth.estimate_gas(gas_tx)

    deploy_tx = contractswan.constructor().build_transaction({
        'chainId': chainId,
        'from': sender,
        'gas': gasAmount,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender)
    })

    #sign the transaction
    sign_txn = web3.eth.account.sign_transaction(deploy_tx, senderkey)
    #send transaction
    tx_hash = web3.eth.send_raw_transaction(sign_txn.rawTransaction)

    #get transaction hash
    txid = str(web3.to_hex(tx_hash))
    transaction_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print('')
    print('Deployed Success TX-ID & Contract Address Result...')
    print(txid)
    print(transaction_receipt.contractAddress)
    time.sleep(10)

#============================================================================
    msg_abi = json.loads('[{"inputs": [{"internalType": "string","name": "newMessage","type": "string"}],"name": "writeMessage","outputs": [],"stateMutability": "nonpayable","type": "function"}]')
    contract_swan = web3.eth.contract(address=web3.to_checksum_address(transaction_receipt.contractAddress), abi=msg_abi)
    #estimate gas limit contract
    gasmsg_tx = contract_swan.functions.writeMessage("test").build_transaction({
        'chainId': chainId,
        'from': sender,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender)
    })
    gasAmount_msg = web3.eth.estimate_gas(gasmsg_tx)

    msg_tx = contract_swan.functions.writeMessage("test").build_transaction({
        'chainId': chainId,
        'from': sender,
        'gas': gasAmount_msg,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender)
    })

    #sign the transaction
    signmsg_txn = web3.eth.account.sign_transaction(msg_tx, senderkey)
    #send transaction
    txmsg_hash = web3.eth.send_raw_transaction(signmsg_txn.rawTransaction)

    #get transaction hash
    txidmsg = str(web3.to_hex(txmsg_hash))
    print('')
    print('Transaction Write Message On Deployed Contract Address TX-ID Result...')
    print(txidmsg)
    time.sleep(10)

    token_addr = web3.to_checksum_address("0x91B25A65b295F0405552A4bbB77879ab5e38166c")
    token_abi = json.loads('[{"inputs": [{"internalType": "address","name": "recipient","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "transfer","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"}]')
    contract_token = web3.eth.contract(address=token_addr, abi=token_abi)

    #generate random evm
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)

    #estimate gas limit contract
    gastoken_tx = contract_token.functions.transfer(web3.to_checksum_address(acct.address), 50000000000000000).build_transaction({
        'chainId': chainId,
        'from': sender,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender)
    })
    gasAmount_tkn = web3.eth.estimate_gas(gastoken_tx)

    token_tx = contract_token.functions.transfer(web3.to_checksum_address(acct.address), 50000000000000000).build_transaction({
        'chainId': chainId,
        'from': sender,
        'gas': gasAmount_tkn,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender)
    })

    #sign the transaction
    signtkn_txn = web3.eth.account.sign_transaction(token_tx, senderkey)
    #send transaction
    txtkn_hash = web3.eth.send_raw_transaction(signtkn_txn.rawTransaction)

    #get transaction hash
    txidtkn = str(web3.to_hex(txtkn_hash))
    print('')
    print('Transaction Send tSWAN Token Success TX-ID Result...')
    print(txidtkn)
    time.sleep(10)
print('==============================================')
print('=        Auto deploy smartcontract           =')
print('=     Auto write function smartcontract      =')
print('=  Auto send tswan token ke random address   =')
print('=              AIRDROP ARCHER                =')
print('=      https://t.me/AirdropFamilyIDN         =')
print('==============================================')
sender = web3.to_checksum_address(input("Input Your EVM Address Swanchain Proxima Testnet : "))
senderkey = input("Input Your EVM Privatekey Swanchain Proxima Testnet : ")
while True:
    MainCall(sender, senderkey)