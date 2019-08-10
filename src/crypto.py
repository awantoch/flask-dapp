import os
import time
import pprint

from web3 import Web3, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware

# connect Web3
w3 = Web3(Web3.HTTPProvider(os.environ['WEB3_PROVIDER']))

# setup for PoA middleware
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# set gas price strategy to built-in "medium" algo (est ~5min per tx)
# see https://web3py.readthedocs.io/en/stable/gas_price.html?highlight=gas
# see https://ethgasstation.info/ API for a more accurate strategy
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# create raw tx object metadata that will be signed
# this fetches current data from node to create a valid tx
# nonce, gasEstimate, gasPrice, and chainId are all needed from a node
def create_raw_tx(_from=w3.eth.accounts[0], _to="", _amount=0):
    amount = w3.toWei(_amount, "gwei") # convert 1.2 ETH to 120000000000 wei
    gasEstimate = w3.eth.estimateGas({ "to": _to, "from": _from, "amount": amount })
    return {
        "to": _to,
        "from": _from,
        "value": amount,
        "gas": gasEstimate,
        "gasPrice": w3.eth.generateGasPrice(),
        "nonce": w3.eth.getTransactionCount(_from),
        "chainId": w3.net.chainId
    }

# helper function to generate and send a transaction
# _amount is the amount in ETH in Gwei, i.e 1.2 ETH instead of 120000000000 wei
def send_tx(_from=w3.eth.accounts[0], _to="", _amount=0):
    tx = create_raw_tx(_from, _to, _amount)
    pprint.pprint(dict(tx))
    return w3.eth.sendTransaction(tx)

# sign a message using Eth private key
def sign_message(account=w3.eth.accounts[0], message=""):
    return w3.eth.sign(account, text=message)

# synchronously wait for transaction receipt based on tx_hash
# this is obviously a bottleneck for scaling, should be async
# block times on Ethereum mainnet are ~12 sec which is the minimum time this fn
# would run on each tx. Ganache is instant, so this is fine for now/development
def wait_for_receipt(w3, tx_hash, poll_interval):
    while True:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        time.sleep(poll_interval)
