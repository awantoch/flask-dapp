import os
import pprint

from contracts import init_abi
from crypto import w3, wait_for_receipt

# keys for the public variables we know are in the smart contract that we want to set and get later
contact_info_keys = ['name', 'email', 'github', 'bitcoin', 'ethereum']

# create contract metadata dictionary
contact_info_meta = { "name": "ContactInfo", "address": os.environ['CONTACT_INFO_ADDRESS'] }

# create contract interface via metadata
contact_info_contract = init_abi(contact_info_meta)

# get gas estimate for function call
def set_contact_info_estimate(fnName, value):
    setValue = getattr(contact_info_contract.functions, fnName)
    return setValue(value).estimateGas()

# create and send transaction to modify contract state
def set_contact_info(fnName, value, account=w3.eth.accounts[0]):
    setValue = getattr(contact_info_contract.functions, fnName)
    tx = setValue(value).transact({
        "from": account,
        "chainId": w3.net.chainId,
        "gas": setValue(value).estimateGas(),
        "gasPrice": w3.eth.generateGasPrice(),
        "nonce": w3.eth.getTransactionCount(account)
    })
    receipt = wait_for_receipt(w3, tx, 0.3) # halting until tx is mined makes this fn synchronous
    print("Transaction sent to mempool: \n")
    pprint.pprint(dict(receipt))
    return { **receipt, "balance": w3.eth.getBalance(account), "operation": fnName }

# fetch a list of public variables and return as a dictionary
def get_contact_info(args=contact_info_keys):
    contact_info = {}
    for arg in args:
        contact_info[arg] = getattr(contact_info_contract.functions, arg)().call()
    return contact_info
